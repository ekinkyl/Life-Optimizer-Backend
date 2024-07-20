from flask_restful import Resource, reqparse
from app import mongo
from bson.objectid import ObjectId

# Parsers
add_activity_parser = reqparse.RequestParser()
add_activity_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_activity_parser.add_argument('activity_type', type=str, required=True, help="Activity Type cannot be blank!")
add_activity_parser.add_argument('description', type=str, required=True, help="Description cannot be blank!")
add_activity_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
add_activity_parser.add_argument('duration', type=float, required=True, help="Duration cannot be blank!")
add_activity_parser.add_argument('calories_burned', type=float, required=True, help="Calories burned cannot be blank!")

add_food_parser = reqparse.RequestParser()
add_food_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_food_parser.add_argument('food_type', type=str, required=True, help="Food Type cannot be blank!")
add_food_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
add_food_parser.add_argument('calories', type=float, required=True, help="Calories cannot be blank!")

add_sleep_parser = reqparse.RequestParser()
add_sleep_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_sleep_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
add_sleep_parser.add_argument('sleep_duration', type=float, required=True, help="Sleep Duration cannot be blank!")
add_sleep_parser.add_argument('sleep_quality', type=str, required=True, help="Sleep Quality cannot be blank!")

# Activity Resource
class AddActivityResource(Resource):
    def post(self):
        args = add_activity_parser.parse_args()
        activity = {
            "user_id": args['user_id'],
            "activity_type": args['activity_type'],
            "description": args['description'],
            "date": args['date'],
            "duration": args['duration'],
            "calories_burned": args['calories_burned']
        }
        mongo.db.activities.insert_one(activity)
        return {'status': 'Activity added'}, 201

# Food Resource
class AddFoodResource(Resource):
    def post(self):
        args = add_food_parser.parse_args()
        food_intake = {
            "user_id": args['user_id'],
            "food_type": args['food_type'],
            "date": args['date'],
            "calories": args['calories']
        }
        mongo.db.food_intake.insert_one(food_intake)
        return {'status': 'Food intake added'}, 201

# Sleep Resource
class AddSleepResource(Resource):
    def post(self):
        args = add_sleep_parser.parse_args()
        sleep_data = {
            "user_id": args['user_id'],
            "date": args['date'],
            "sleep_duration": args['sleep_duration'],
            "sleep_quality": args['sleep_quality']
        }
        mongo.db.sleep_data.insert_one(sleep_data)
        return {'status': 'Sleep data added'}, 201

# Health Data Resource
class HealthDataResource(Resource):
    def get(self, user_id):
        health_data = mongo.db.health_data.find({'user_id': user_id})
        return [{'id': str(data['_id']), 'date': data['date'], 'calories': data['calories'], 'sleep_hours': data['sleep_hours'], 'food_type': data['food_type'], 'sports_type': data['sports_type']} for data in health_data]

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
