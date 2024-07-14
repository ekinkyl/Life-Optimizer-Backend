#Functionality: This file initializes the Flask application and its extensions, such as SQLAlchemy for database interactions, Migrate for handling database migrations, and Flask-RESTful for creating REST APIs.
#Content: This file typically contains the application factory function create_app() which sets up the app with configurations and initializes extensions.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy #This is an ORM (Object Relational Mapper) that provides a high-level abstraction for database manipulation.
from flask_migrate import Migrate # This is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
from flask_restful import Api #This is a class from Flask-RESTful that helps in creating RESTful APIs.
from config import Config #This is a custom configuration class (defined in config.py) that holds configuration variables.

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app(): #create the application instance inside a function. This allows for easier configuration and testing.
    app = Flask(__name__) #Creates an instance of the Flask class. The __name__ argument is used to determine the root path for the application.
    app.config.from_object(Config) #: Configures the Flask app using the configuration variables defined in the Config class.

    #initialization
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    from app.resources.user import UserResource #Imports the UserResource class from app/resources/user.py. This class defines how to handle requests to the /api/users endpoint.
    api.add_resource(UserResource, '/api/users') #Registers the UserResource with the API. This means that requests to /api/users will be handled by the UserResource class.

    return app
