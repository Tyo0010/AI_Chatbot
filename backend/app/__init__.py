from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate(db)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'aichatbotforpersonalutilizing'  # Use an environment variable in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600          # 1 hour
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000      # 30 days

    with app.app_context():
        # Initialize DB and Migrations
        db.init_app(app)
        migrate.init_app(app, db)

        # Initialize JWT
        jwt = JWTManager(app)

        # Register Blueprints
        from app.views import blueprint as views_bp
        app.register_blueprint(views_bp)

        from app.errors import blueprint as errors_bp
        app.register_blueprint(errors_bp)

        db.create_all()
        db.session.commit()

    return app
