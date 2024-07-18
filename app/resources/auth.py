# app/resources/auth.py

from flask_restful import Resource, reqparse
from app.models import User, db
from flask_jwt_extended import create_access_token

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
register_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
register_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
login_parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

class RegisterResource(Resource):
    def post(self):
        args = register_parser.parse_args()
        user = User(username=args['username'], email=args['email'], password_hash=args['password'])
        db.session.add(user)
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email}, 201

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args['email'], password_hash=args['password']).first()
        if not user:
            return {'message': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return {'access_token': access_token}, 200
