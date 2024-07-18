from flask_restful import Resource, reqparse
from app import mongo

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
parser.add_argument('age', type=int, required=True, help="Age cannot be blank!")
parser.add_argument('height', type=int, required=True, help="Height cannot be blank!")
parser.add_argument('weight', type=float, required=True, help="Weight cannot be blank!")
parser.add_argument('gender', type=str, required=True, help="Gender cannot be blank!")

class UserResource(Resource):
    def get(self):
        users = mongo.db.users.find()
        return [{'id': str(user['_id']), 'username': user['username'], 'email': user['email'], 'age': user['age'], 'height': user['height'], 'weight': user['weight'], 'gender': user['gender']} for user in users]

    def post(self):
        args = parser.parse_args()
        user = {
            'username': args['username'],
            'email': args['email'],
            'password_hash': args['password'],
            'age': args['age'],
            'height': args['height'],
            'weight': args['weight'],
            'gender': args['gender']
        }
        mongo.db.users.insert_one(user)
        return {'id': str(user['_id']), 'username': user['username'], 'email': user['email'], 'age': user['age'], 'height': user['height'], 'weight': user['weight'], 'gender': user['gender']}, 201
