from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os
from common.logs.logger import logger


db = SQLAlchemy()

class DatabaseConfig:
    """Centralized database configuration for any service"""
    @staticmethod
    def get_uri(username, password, host, port, database):
        return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

def init_db(app, db_name=None):
    """Initialize the database with Flask app."""
    # Load default configurations from environment variables
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = db_name or os.getenv("DB_NAME")  # Use db_name if provided, otherwise default

    # Set database URI dynamically
    app.config["SQLALCHEMY_DATABASE_URI"] = DatabaseConfig.get_uri(username, password, host, port, database)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            # logger.info("Database tables created successfully!")
            app.config['DB_AVAILABLE'] = True
    except OperationalError as e:
        # Log the error and fallback to degraded mode
        logger.error(f"Database connection failed: {e}")
        app.config['DB_AVAILABLE'] = False
        logger.critical("Running in degraded mode: database operations disabled.")
