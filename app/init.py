from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    from app.resources.user import UserResource
    from app.resources.health_data import HealthDataResource
    from app.resources.auth import RegisterResource, LoginResource 

    api.add_resource(UserResource, '/api/users')
    api.add_resource(HealthDataResource, '/api/health_data')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')

    return app
app = create_app()
