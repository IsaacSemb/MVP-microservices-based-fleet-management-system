from flask import Flask
from sqlalchemy import text
from flask_cors import CORS  
from dotenv import load_dotenv
import os
import sys

# Load global environment variables
load_dotenv("../.env") 

# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(root_path) 

# Import common modules
from common.database.db_utils import db, init_db
from common.logs.logger import logger


# Flask application configuration
APP_PORT = os.getenv("SERVICE_1_PORT") 


# Import models and routes
# from models import Driver
from services.service1_driver_management.routes import driver_blueprint 

# Create an instance of the Flask app
app = Flask(__name__)

# Dynamically initialize the database with service db name
SERVICE_1_DB_NAME = os.getenv("SERVICE_1_DB_NAME") 
init_db(app, db_name=SERVICE_1_DB_NAME)
CORS(app)

# Landing page for the server
@app.route("/")
def home():
    logger.info(f"Server listening at port {APP_PORT}!")
    return f"<h1>Server listening at port {APP_PORT}! [ DB -- {app.config['DB_AVAILABLE']}]</h1>"

# Route to test database connection
@app.route("/dbtest")
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        logger.info("checked database health and it is fine")
        return "Database connection successful!", 200
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return f"Database connection failed: {e}", 500


# Register blueprints
app.register_blueprint(driver_blueprint)

print(os.getenv("DEVELOPER"))

if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=APP_PORT,
        debug=os.getenv("FLASK_ENV") == "development"
    )
