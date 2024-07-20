# app/init.py

from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from config import Config

# Initialize PyMongo instance
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB connection
    mongo.init_app(app)

    # Import resources
    from app.resources.user import UserResource
    from app.resources.health_data import HealthDataResource
    from app.resources.auth import RegisterResource, LoginResource
    from app.resources.friends import AddFriendResource, GetFriendsActivitiesResource
    from app.resources.blog import BlogPostResource, UserPreferencesResource, BlogSuggestionsResource

    # Initialize Flask-RESTful API
    api = Api(app)
    
    # Add resources to API
    api.add_resource(UserResource, '/api/users')
    api.add_resource(HealthDataResource, '/api/health_data')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(AddFriendResource, '/api/friends')
    api.add_resource(GetFriendsActivitiesResource, '/api/friends/activities/<string:user_id>')
    api.add_resource(BlogPostResource, '/api/blog_posts')
    api.add_resource(UserPreferencesResource, '/api/user_preferences')
    api.add_resource(BlogSuggestionsResource, '/api/blog_suggestions/<string:user_id>')

    return app
