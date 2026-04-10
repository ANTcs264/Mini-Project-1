import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # On Vercel, use in‑memory SQLite (no file persistence)
    if os.environ.get('VERCEL_ENV'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        # Local development – use file database inside data/
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'database', 'game.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True if not os.environ.get('VERCEL_ENV') else False