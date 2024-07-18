# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from flask_restful import Api

mongo = PyMongo()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    from app.resources.user import UserResource
    from app.resources.health_data import HealthDataResource
    from app.resources.auth import RegisterResource, LoginResource

    api.add_resource(UserResource, '/api/users')
    api.add_resource(HealthDataResource, '/api/health_data')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')

    api.init_app(app)  # Make sure to initialize API after adding resources

    return app
