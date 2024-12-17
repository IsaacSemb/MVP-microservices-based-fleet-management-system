from flask import Blueprint, jsonify, request
from services.service2_vehicle_management.models import Vehicle
from common.database.db_utils import db
from sqlalchemy.exc import SQLAlchemyError
from common.logs.logger import logger
from common.message_broker.rabbitmq_utils import RabbitMQ
 

vehicle_blueprint = Blueprint("vehicle_bp", __name__)

@vehicle_blueprint.route('/vehicles', methods=['POST'])
def register_vehicle():
    try:
        data = request.get_json()
        new_vehicle = Vehicle(
            make=data["make"],
            model=data["model"],
            reg_no=data["reg_no"],
            fuel_type=data["fuel_type"],
            vehicle_type=data["vehicle_type"],
            status=data["status"]
        )
        # db.session.add(new_vehicle)
        # db.session.commit()
        
        logger.info(f"new vehicle added to the database: [vehicle_plate:{new_vehicle.reg_no}]")
        
        try:
            # Publish to the broker
            new_vehicle_created_message = {
                "event_type": "vehicle_created",
                "data": new_vehicle.to_dict()
            }
            
            # get broker
            broker = RabbitMQ()
            broker.publish_message(
                exchange='vehicle_created_fanout_exchange',
                exchange_type='fanout',
                routing_key='',
                message=new_vehicle_created_message
            )
            logger.info(f"published new vehicle: {new_vehicle.vehicle_id}")
        except Exception as e:
            # Log broker error
            logger.error(f"Error publishing message to broker: {str(e)}")
            return jsonify({"message": "vehicle created but failed to notify listeners"}), 201
        
        return jsonify({"message": "Vehicle registered successfully!"}), 201
    except SQLAlchemyError as sql_err:
        db.session.rollback()
        logger.error(f"Error creating vehicle: {str(sql_err)}")
        return jsonify({"error": f"Database error: {str(sql_err)}"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating vehicle: {str(e)}")
        return jsonify({"error": str(e)}), 400

@vehicle_blueprint.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    try:
        # Fetch the query parameter to decide the response type
        response_type = request.args.get('response_type', 'full').lower()  # Default to 'full'
        
        all_vehicles = Vehicle.query.all()
        vehicle_objects = [vehicle.to_dict() for vehicle in all_vehicles]
        
        # Initialize summary variables
        total_count = len(vehicle_objects)
        vehicle_type_counts = {}
        total_available = 0
        total_unavailable = 0

        # Loop through the vehicles in the database
        for vehicle in vehicle_objects:
            # Get the vehicle type, capitalize it for consistent formatting
            vehicle_type = vehicle['vehicle_type'].capitalize()

            # Initialize counts for this vehicle type if not already present
            if vehicle_type not in vehicle_type_counts:
                vehicle_type_counts[vehicle_type] = {"available": 0, "unavailable": 0}

            # Increment counts based on availability
            if vehicle['status'].lower()=='available':
                vehicle_type_counts[vehicle_type]["available"] += 1
                total_available += 1
            else:
                vehicle_type_counts[vehicle_type]["unavailable"] += 1
                total_unavailable += 1
        
        vehicle_type_counts["total_vehicles"] = {
            "available": total_available,
            "unavailable": total_unavailable
        }

        # Prepare the summary
        summary = {
            "total_vehicles": total_count,
            "total_by_type": vehicle_type_counts
        }

        # Return the response based on the requested type
        if response_type == 'summary':
            return jsonify({"summary": summary}), 200
        elif response_type == 'details':
            return jsonify({"details": vehicle_objects}), 200
        else:
            # Default full response
            response = {
                "summary": summary,
                "details": vehicle_objects
            }
            return jsonify(response), 200
        
        
    except SQLAlchemyError as sql_err:
        logger.error(f"Error fetching vehicles: {str(sql_err)}")
        return jsonify({"error": f"Database error: {str(sql_err)}"}), 500
    except Exception as e:
        logger.error(f"Error fetching vehicles: {str(e)}")
        return jsonify({"error": str(e)}), 400

    

@vehicle_blueprint.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            return jsonify(vehicle.to_dict()), 200
        return jsonify({"error": "Vehicle not found"}), 404
    except SQLAlchemyError as sql_err:
        logger.error(f"Error fetching vehicles: {str(sql_err)}")
        return jsonify({"error": f"Database error: {str(sql_err)}"}), 500
    except Exception as e:
        logger.error(f"Error fetching vehicles: {str(e)}")
        return jsonify({"error": str(e)}), 400

@vehicle_blueprint.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return jsonify({"message": "Vehicle deleted successfully"}), 200
        return jsonify({"error": "Vehicle not found"}), 404
    except SQLAlchemyError as sql_err:
        db.session.rollback()
        logger.error(f"Error fetching vehicles: {str(sql_err)}")
        return jsonify({"error": f"Database error: {str(sql_err)}"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error fetching vehicles: {str(e)}")
        return jsonify({"error": str(e)}), 400

@vehicle_blueprint.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        new_vehicle_data = request.get_json()
        
        vehicle.make = new_vehicle_data.get("make", vehicle.make)
        vehicle.model = new_vehicle_data.get("model", vehicle.model)
        vehicle.reg_no = new_vehicle_data.get("reg_no", vehicle.reg_no)
        vehicle.fuel_type = new_vehicle_data.get("fuel_type", vehicle.fuel_type)
        vehicle.vehicle_type = new_vehicle_data.get("vehicle_type", vehicle.vehicle_type)
        if "status" in new_vehicle_data:
            vehicle.status = new_vehicle_data["status"]
        db.session.commit()
        return jsonify({"message": "Vehicle updated successfully"}), 200
    except SQLAlchemyError as sql_err:
        db.session.rollback()
        logger.error(f"Error fetching vehicles: {str(sql_err)}") 
        return jsonify({"error": f"Database error: {str(sql_err)}"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error fetching vehicles: {str(e)}")        
        return jsonify({"error": str(e)}), 400
