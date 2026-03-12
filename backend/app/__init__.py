from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure the database directory exists
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            print(f"📁 Created database directory: {db_dir}")
        except Exception as e:
            print(f"⚠️ Could not create directory {db_dir}: {e}")
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    from app.routes.game_routes import game_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(game_bp, url_prefix='/api/game')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            print("Please check:")
            print("  1. Database directory permissions")
            print("  2. Path in SQLALCHEMY_DATABASE_URI")
            print("  3. Disk space availability")
    
    return app