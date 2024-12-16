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

# Import shared modules
from shared.database.db_utils import db, init_db

# Flask application configuration
APP_PORT = os.getenv("SERVICE_1_PORT")


# Import models and routes
from models import Driver
from routes import driver_blueprint

# Create an instance of the Flask app
app = Flask(__name__)

# Dynamically initialize the database with service db name
SERVICE_1_DB_NAME = os.getenv("SERVICE_1_DB_NAME")
init_db(app, db_name=SERVICE_1_DB_NAME)
CORS(app)

# Landing page for the server
@app.route("/")
def home():
    return f"Server listening at port {APP_PORT}!"

# Route to test database connection
@app.route("/dbtest")
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "Database connection successful!", 200
    except Exception as e:
        return f"Database connection failed: {e}", 500

# Register blueprints
app.register_blueprint(driver_blueprint)

# Consumer necessities
from shared.message_broker.consumer_manager import start_consumer_processes 
from consumer_objects import SERVICE_1_CONSUMERS

# Running the app
if __name__ == "__main__":
    start_consumer_processes(consumers=SERVICE_1_CONSUMERS)
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=int(APP_PORT),
        debug=os.getenv("FLASK_ENV") == "development"
    )
 