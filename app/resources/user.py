from flask_restful import Resource #Resource is a base class for creating RESTful resources in Flask-RESTful.
from app.models import User #User model is used to interact with the User table in the database.

class UserResource(Resource): #becomes a RESTful resource that can handle HTTP requests.
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
