import os

class Config:
    # Update with your actual MongoDB URI
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/myDatabase')
