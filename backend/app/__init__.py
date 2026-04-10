from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    from app.routes.game_routes import game_bp
    app.register_blueprint(game_bp, url_prefix='/api/game')

    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")

    return app