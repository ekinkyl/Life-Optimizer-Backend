from flask_restful import Resource, reqparse
from app import mongo
from bson.objectid import ObjectId

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
parser.add_argument('sleep_hours', type=float, required=True, help="Sleep hours cannot be blank!")
parser.add_argument('food_type', type=str, required=True, help="Food type cannot be blank!")
parser.add_argument('sports_type', type=str, required=True, help="Sports type cannot be blank!")

class HealthDataResource(Resource):
    def get(self, user_id):
        health_data = mongo.db.health_data.find({'user_id': user_id})
        return [{'id': str(data['_id']), 'date': data['date'], 'calories': data['calories'], 'sleep_hours': data['sleep_hours'], 'food_type': data['food_type'], 'sports_type': data['sports_type']} for data in health_data]

    def post(self):
        args = parser.parse_args()
        food_calories = mongo.db.food_calories.find_one({'food_type': args['food_type'].lower()})
        sport_calories = mongo.db.sport_calories.find_one({'sport_type': args['sports_type'].lower()})
        net_calories = (food_calories['calories_per_100g'] if food_calories else 0) - (sport_calories['calories_per_kg'] if sport_calories else 0)

        data = {
            'user_id': args['user_id'],
            'date': args['date'],
            'sleep_hours': args['sleep_hours'],
            'food_type': args['food_type'],
            'sports_type': args['sports_type'],
            'calories': net_calories
        }
        result = mongo.db.health_data.insert_one(data)
        return {'id': str(result.inserted_id), 'user_id': data['user_id'], 'date': data['date'], 'calories': data['calories'], 'sleep_hours': data['sleep_hours'], 'food_type': data['food_type'], 'sports_type': data['sports_type']}, 201

    def put(self, data_id):
        args = parser.parse_args()
        food_calories = mongo.db.food_calories.find_one({'food_type': args['food_type'].lower()})
        sport_calories = mongo.db.sport_calories.find_one({'sport_type': args['sports_type'].lower()})
        net_calories = (food_calories['calories_per_100g'] if food_calories else 0) - (sport_calories['calories_per_kg'] if sport_calories else 0)

        data = {
            'date': args['date'],
            'sleep_hours': args['sleep_hours'],
            'food_type': args['food_type'],
            'sports_type': args['sports_type'],
            'calories': net_calories
        }

        result = mongo.db.health_data.update_one({'_id': ObjectId(data_id)}, {'$set': data})
        if result.matched_count == 0:
            return {'message': 'Data not found'}, 404
        return {'message': 'Data updated successfully'}, 200

    def delete(self, data_id):
        result = mongo.db.health_data.delete_one({'_id': ObjectId(data_id)})
        if result.deleted_count == 0:
            return {'message': 'Data not found'}, 404
        return {'message': 'Data deleted successfully'}, 204
