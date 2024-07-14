from flask_restful import Resource, reqparse
from app.models import HealthData, db

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True, help="User ID cannot be blank!")
parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
parser.add_argument('sleep_hours', type=float, required=True, help="Sleep hours cannot be blank!")
parser.add_argument('food_type', type=str, required=True, help="Food type cannot be blank!")
parser.add_argument('sports_type', type=str, required=True, help="Sports type cannot be blank!")
#parser.add_argument('steps', type=int, required=True, help="Steps cannot be blank!")
#parser.add_argument('calories', type=int, required=True, help="Calories cannot be blank!")

class HealthDataResource(Resource):
    def get(self, user_id):
        health_data = HealthData.query.filter_by(user_id=user_id).all()
        return [{'id': data.id, 'date': data.date, 'steps': data.steps, 'calories': data.calories, 'sleep_hours': data.sleep_hours, 'food_type': data.food_type, 'sports_type': data.sports_type} for data in health_data]
    
    def post(self):
        args = parser.parse_args()
        data = HealthData(
            user_id=args['user_id'], 
            date=args['date'], 
            sleep_hours=args['sleep_hours'],
            food_type=args['food_type'], 
            sports_type=args['sports_type'],
            #steps=args['steps'], 
            #calories=args['calories']
        )
        db.session.add(data)
        db.session.commit()
        return {'id': data.id, 'user_id': data.user_id, 'date': data.date, 'sleep_hours': data.sleep_hours, 'food_type': data.food_type, 'sports_type': data.sports_type}, 201
    
    def put(self, data_id):
        args = parser.parse_args()
        data = HealthData.query.get_or_404(data_id)
        data.sleep_hours = args['sleep_hours']
        data.food_type = args['food_type']
        data.sports_type = args['sports_type']
        #data.steps = args['steps']
        #data.calories = args['calories']
        db.session.commit()
        return {'id': data.id, 'user_id': data.user_id, 'date': data.date, 'sleep_hours': data.sleep_hours, 'food_type': data.food_type, 'sports_type': data.sports_type}, 200
    
    def delete(self, data_id):
        data = HealthData.query.get_or_404(data_id)
        db.session.delete(data)
        db.session.commit()
        return '', 204
