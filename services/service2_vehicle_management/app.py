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
APP_PORT = os.getenv("SERVICE_2_PORT")

# model and routes
from services.service2_vehicle_management.routes import vehicle_blueprint

# creating an instance of server
app = Flask(__name__)

# Initialize db with app 
SERVICE_2_DB_NAME = os.getenv("SERVICE_2_DB_NAME")
init_db(app, db_name=SERVICE_2_DB_NAME)
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
        return f"Database connection failed: {e}", 500

# registering the blueprints
app.register_blueprint(vehicle_blueprint)


# Running the app
if __name__ == "__main__":
    
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=int(APP_PORT),
        debug=os.getenv("FLASK_ENV") == "development"
    )
