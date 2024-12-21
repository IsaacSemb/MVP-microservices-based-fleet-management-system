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
from common.database.db_utils import db, init_db
from common.logs.logger import logger

# Flask application configuration
APP_PORT = os.getenv("SERVICE_4_PORT")

# import the models and routes
from routes import maintenance_logs_bp

# creating an instance of server
app = Flask(__name__)

# Dynamically initialize the database with service db name
SERVICE_4_DB_NAME = os.getenv("SERVICE_4_DB_NAME")
print(SERVICE_4_DB_NAME,"################__________")
init_db(app, db_name=SERVICE_4_DB_NAME)
CORS(app)

# landing page for server
@app.route("/")
def home():
    return f"server listening at port {APP_PORT}!"

#route to test our database connection
@app.route("/dbtest") 
def test_db():
    try:
        # Test the database connection
        db.session.execute(text("SELECT 1"))
        return "Database connection successful!", 200
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return f"Database connection failed: This service is unavailable", 503

# registering the blueprints
app.register_blueprint(maintenance_logs_bp)

# Running the app
if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=int(APP_PORT),
        debug=os.getenv("FLASK_ENV") == "development"
    )