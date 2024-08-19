import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017'
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_default_secret_key_here'  
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO') 