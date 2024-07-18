from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # Add gender column

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(64), nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    food_type = db.Column(db.String(64), nullable=False)
    sports_type = db.Column(db.String(64), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('health_data', lazy=True))

class FoodCalories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String(64), unique=True, nullable=False)
    calories_per_100g = db.Column(db.Float, nullable=False)

class SportCalories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_type = db.Column(db.String(64), unique=True, nullable=False)
    calories_per_kg = db.Column(db.Float, nullable=False)

class SleepLifestyleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sleep_duration = db.Column(db.Float, nullable=False)
    physical_activity_level = db.Column(db.String(64), nullable=False)
    sleep_quality = db.Column(db.String(64), nullable=False)
