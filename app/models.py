# Defines the database models

from app import db #db object is an instance of SQLAlchemy that was initialized in app/__init__.py.

class User(db.Model): #This defines a new class User that inherits from db.Model. By inheriting from db.Model, the User class becomes a model in SQLAlchemy, representing a table in the database.
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True, nullable=False) #Both username and email have unique constraints to ensure no duplicates.
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    #Unique Constraints: Both username and email have unique constraints to ensure no duplicates.
    #indexes on username and email to improve query performance
    #Non-nullable Constraints: Both username and email are required fields (cannot be null).
