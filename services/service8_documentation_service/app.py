from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os, sys

# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(root_path) 

from common.logs.logger import logger


app = Flask(__name__)

# Configuration for Swagger UI
SWAGGER_URL = "/docs"  # Base URL for Swagger UI
DOC_URL = "/static/swagger_docs/fleet_manager.yml"  # Path to your YAML file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    DOC_URL,
    config={"app_name": "Fleet Manager API Documentation"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Route to serve the Swagger YAML file
@app.route(DOC_URL, methods=["GET"])
def serve_swagger_yaml():
    """Serve the Swagger YAML file."""
    return send_from_directory("static/swagger_docs", "fleet_manager.yml")

APP_PORT = os.getenv("SERVICE_8_PORT") 


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=APP_PORT,
        debug=os.getenv("FLASK_ENV") == "development"
    )
