import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Simple database in current directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///game_database.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True