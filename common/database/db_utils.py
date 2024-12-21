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
    host = os.getenv("DB_HOST", "localhost")
    username = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("SERVICE_1_DB_NAME", db_name)
    port = os.getenv("DB_PORT", 3306)
    
    
    if not database:
        logger.error("Database name is not provided. Check environment variables or db_name argument.")
        return


    # Set database URI dynamically
    app.config["SQLALCHEMY_DATABASE_URI"] = DatabaseConfig.get_uri(username, password, host, port, database)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    logger.info(f"Connecting to database: {database} at {host}:{port}")
    
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
