from flask import Flask, send_from_directory
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from .config import DevelopmentConfig, TestingConfig
from .auth import auth_bp  
from .post import post_bp
from app.json_encoder import MongoJSONEncoder
from .extensions import mongo
import os

from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()
SWAGGER_URL="/swagger"
API_URL='/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Blog API'
    }
)

def create_app():
    """
    Create Flask application, configuration will be based on given environment variable
    """
    env = os.environ.get('FLASK_ENV', 'DEV')
  
    if env == 'TEST':
        app_config = TestingConfig
    else:
        app_config = DevelopmentConfig
 
    app = Flask(__name__, static_folder='static')
    app.config.from_object(app_config)
    app.json_encoder = MongoJSONEncoder
    mongo.init_app(app)
    try:
        print("MongoDB is connected and ready.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
  
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/')

    return app
