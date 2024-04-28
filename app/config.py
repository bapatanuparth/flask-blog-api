import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    """Set Flask configuration vars from .env file."""

    MONGO_URI =os.getenv('MONGO_URI') 
    SECRET_KEY=os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI')  
    SECRET_KEY=os.getenv('SECRET_KEY')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST')
    SECRET_KEY=os.getenv('SECRET_KEY')