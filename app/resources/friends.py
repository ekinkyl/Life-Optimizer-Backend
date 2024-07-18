from flask_restful import Resource, reqparse
from app import mongo

# Parser for adding friends
add_friend_parser = reqparse.RequestParser()
add_friend_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_friend_parser.add_argument('friend_id', type=str, required=True, help="Friend ID cannot be blank!")

# Parser for adding activities
add_activity_parser = reqparse.RequestParser()
add_activity_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_activity_parser.add_argument('activity_type', type=str, required=True, help="Activity Type cannot be blank!")
add_activity_parser.add_argument('description', type=str, required=True, help="Description cannot be blank!")
add_activity_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")
add_activity_parser.add_argument('duration', type=float, required=True, help="Duration cannot be blank!")
add_activity_parser.add_argument('calories_burned', type=float, required=True, help="Calories burned cannot be blank!")

# Parser for adding food intake
add_food_parser = reqparse.RequestParser()
add_food_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_food_parser.add_argument('food_type', type=str, required=True, help="Food Type cannot be blank!")
add_food_parser.add_argument('calories', type=float, required=True, help="Calories cannot be blank!")
add_food_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")

# Parser for adding sleep data
add_sleep_parser = reqparse.RequestParser()
add_sleep_parser.add_argument('user_id', type=str, required=True, help="User ID cannot be blank!")
add_sleep_parser.add_argument('sleep_duration', type=float, required=True, help="Sleep Duration cannot be blank!")
add_sleep_parser.add_argument('date', type=str, required=True, help="Date cannot be blank!")

class AddFriendResource(Resource):
    def post(self):
        args = add_friend_parser.parse_args()
        friend = {
            "user_id": args['user_id'],
            "friend_id": args['friend_id']
        }
        mongo.db.friends.insert_one(friend)
        return {'status': 'Friend added'}, 201

class GetFriendsActivitiesResource(Resource):
    def get(self, user_id):
        friends = mongo.db.friends.find({'user_id': user_id})
        friend_ids = [friend['friend_id'] for friend in friends]
        activities = mongo.db.activities.find({'user_id': {'$in': friend_ids}})
        return [{'activity_type': activity['activity_type'], 'description': activity['description'], 'date': activity['date'], 'duration': activity['duration'], 'calories_burned': activity['calories_burned']} for activity in activities]

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

class AddFoodIntakeResource(Resource):
    def post(self):
        args = add_food_parser.parse_args()
        food = {
            "user_id": args['user_id'],
            "food_type": args['food_type'],
            "calories": args['calories'],
            "date": args['date']
        }
        mongo.db.food_intake.insert_one(food)
        return {'status': 'Food intake added'}, 201

class AddSleepDataResource(Resource):
    def post(self):
        args = add_sleep_parser.parse_args()
        sleep = {
            "user_id": args['user_id'],
            "sleep_duration": args['sleep_duration'],
            "date": args['date']
        }
        mongo.db.sleep_data.insert_one(sleep)
        return {'status': 'Sleep data added'}, 201
