from flask import Blueprint, jsonify, request
from models import Driver
from common.database.db_utils import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import Enum
from common.logs.logger import logger
from common.message_broker.rabbitmq_utils import RabbitMQ


# creation of ther blue print for routing
driver_blueprint = Blueprint("driver_bp", __name__)

# creating a new driver
@driver_blueprint.route('/drivers', methods=['POST'])
def create_driver():
    try:
        # Incoming data to the server
        data = request.get_json()
        
        # Manipulate data to create a new driver object
        new_driver = Driver(
            first_name=data["first_name"],
            last_name=data["last_name"],
            sex=data["sex"],
            license_no=data["license_no"],
            contact_info=data["contact_info"],
            status=data.get('status', 'available')  # Default to 'available' if not provided
        )

        # Add the new driver to the database session
        # db.session.add(new_driver)

        # Commit the transaction
        # db.session.commit()
        
        logger.info("new driver created")
        logger.info(new_driver)
        
        # send to to broker
        try:
            # create the message to send to broker
            new_driver_created_message = {
            "event_type": "driver_created",
            "data": new_driver.to_dict()
            }
            logger.info(new_driver_created_message)
            
            # get broker
            broker = RabbitMQ()
            broker.publish_message(
                exchange='driver_created_fanout_exchange',
                exchange_type='fanout',
                routing_key='',
                message=new_driver_created_message
            )
            logger.info(f"published new driver: {new_driver.driver_id}")
        except Exception as e:
            # Log broker error
            logger.error(f"Error publishing message to broker: {str(e)}")
            return jsonify({"message": "Driver created but failed to notify listeners"}), 201

        # Return success message
        return jsonify({"message": "Driver created successfully!", "driver": new_driver.to_dict()}), 201

    # case of missing keys in the input data
    except KeyError as e:
        db.session.rollback() 
        missing_field = str(e).strip("'")
        logger.debug(f"Missing field: {missing_field}")
        return jsonify({"error": f"Missing required field: {missing_field}"}), 400

    # case of database errors from mysql
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback the transaction
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "An error occurred while saving the driver to the database. Please try again."}), 500

    except Exception as e:
        # Handle any other unexpected errors
        db.session.rollback()  # Rollback the transaction
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


@driver_blueprint.route('/drivers', methods=['GET'])
def get_all_drivers():
    try:
        # Fetch the query parameter to decide the response type
        response_type = request.args.get('response_type', 'full').lower()  # Default to 'full'

        # Query all drivers from the database
        all_drivers = Driver.query.all()

        # Convert driver objects to details dictionaries
        driver_objects = [driver.to_dict() for driver in all_drivers]
                
        # Dynamically get the enum options from the Driver model
        status_enum_values = Driver.__table__.columns['status'].type.enums

        # Initialize summary variables
        total_count = len(driver_objects)
        status_summary = {status: 0 for status in status_enum_values}

        # Loop through the drivers to count statuses dynamically
        for driver in driver_objects:
            driver_status = driver['status'].lower()
            if driver_status in status_summary:
                status_summary[driver_status] += 1

        # Prepare the summary
        summary = {
            "total_drivers": total_count,
            "status_summary": status_summary
        }

        # Return the response based on the requested type
        if response_type == 'summary':
            logger.info("request for summarized drivers")
            return jsonify({"summary": summary}), 200
        
        elif response_type == 'details':
            logger.info("request for detailed drivers")
            return jsonify({"details": driver_objects}), 200
        
        else:
            # Default full response
            response = {
                "summary": summary,
                "details": driver_objects
            }
            logger.info("request for both detailed and summarized drivers")
            return jsonify(response), 200

    except SQLAlchemyError as e:
        # Log the error for debugging
        logger.error(f"Database error occurred: {str(e)}")

        # Return a JSON error response with a 500 status code
        return jsonify({"error": "An error occurred while fetching drivers. Please try again later."}), 500

    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error occurred: {str(e)}")

        # Return a generic error response
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@driver_blueprint.route('/drivers/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    try:
        # Query the driver by ID
        driver = Driver.query.get(driver_id)
        
        # Check if the driver exists
        if driver:
            driver_object = driver.to_dict()
            return jsonify(driver_object), 200
        else:
            return jsonify({"error": "Driver not found"}), 404

    except SQLAlchemyError as e:
        # Handle database-related errors
        logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching the driver. Please try again later."}), 500

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@driver_blueprint.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    try:
        # Search for the driver in the database
        driver = Driver.query.get(driver_id)

        # If the driver is found, delete it
        if driver:
            db.session.delete(driver)
            db.session.commit()
            return jsonify({"message": "Driver deleted successfully"}), 200

        # If the driver is not found, return 404
        return jsonify({"error": "Driver not found"}), 404

    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()
        logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the driver. Please try again later."}), 500

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

        
@driver_blueprint.route('/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    try:
        # Search the database for the driver
        driver = Driver.query.get(driver_id)

        # If the driver is not found, return 404
        if not driver:
            return jsonify({"error": "Driver not found"}), 404

        # Get the new data from the request body
        new_driver_data = request.get_json()

        # Update only the fields provided in the request
        driver.first_name = new_driver_data.get("first_name", driver.first_name)
        driver.last_name = new_driver_data.get("last_name", driver.last_name)
        driver.sex = new_driver_data.get("sex", driver.sex)
        driver.license_no = new_driver_data.get("license_no", driver.license_no)
        driver.contact_info = new_driver_data.get("contact_info", driver.contact_info)
        driver.status = new_driver_data.get("status", driver.status)

        # Try to commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Driver updated successfully"}), 200

    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()
        logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while updating the driver. Please try again later."}), 500

    except Exception as e:
        # Handle unexpected errors
        db.session.rollback()
        logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    