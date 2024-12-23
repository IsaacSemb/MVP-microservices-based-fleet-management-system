from flask import Blueprint, request, jsonify
from services.service3_assignments.models import Assignment
from common.database.db_utils import db
import os
from common.message_broker.rabbitmq_utils import RabbitMQ
from common.logs.logger import logger


# service urls
SERVICE_1_URL = os.getenv('SERVICE_1_URL')
SERVICE_2_URL = os.getenv('SERVICE_2_URL')

assignment_bp = Blueprint('assignment_bp', __name__)

# Route to add a new fleet assignment
@assignment_bp.route('/assignments', methods=['POST'])
def add_assignment():
    try:
        data = request.json
        driver_id = data.get('driver_id')
        vehicle_id = data.get('vehicle_id')

            # WE NEED TO VALIDATE THE VEHICLE AND DRIVER IDS
        driver_exists, response_code = True , 200 # response_code,_ = validate_and_fetch_resource(url=f"{SERVICE_1_URL}/drivers",resource_id=driver_id)
        vehicle_exists, response_code = True , 200 # response_code,_ = validate_and_fetch_resource(url=f"{SERVICE_2_URL}/vehicles",resource_id=vehicle_id)

        if not driver_exists:
            return jsonify({"error": "Driver not found in driver service"}), response_code
        if not vehicle_exists:
            return jsonify({"error": "Vehicle not found in vehicle service"}), response_code

        # Create new assignment
        new_assignment = Assignment(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_date_time=data.get('start_date_time'),
            end_date_time=data.get('end_date_time'),
            status=data.get('status', 'scheduled')  # Default to 'scheduled'
        )

        # Add to database
        db.session.add(new_assignment)
        db.session.commit()

        
        try:
            # Publish to the broker
            new_assignment_created_message = {
                "event_type": "assignment_created",
                "data": new_assignment.to_dict()
            }
            
            # get broker
            broker = RabbitMQ()
            broker.publish_message(
                exchange='assignment_created_fanout_exchange',
                exchange_type='fanout',
                routing_key='',
                message=new_assignment_created_message
            )
            logger.info(f"published new assignment: {new_assignment.assignment_id}")
        except Exception as e:
            # Log broker error
            logger.error(f"Error publishing message to broker: {str(e)}")
            return jsonify({"message": "Assignment created but failed to notify listeners", "assignment": new_assignment.to_dict()}), 201

        # Return success response
        return jsonify({"message": "Assignment created successfully", "assignment": new_assignment.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating assignment: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


# Route to get all assignments
@assignment_bp.route('/assignments', methods=['GET'])
def get_all_assignments():
    try:
        assignments = Assignment.query.all()
        assignment_list = [
            {
                "assignment_id": assignment.assignment_id,
                "driver_id": assignment.driver_id,
                "vehicle_id": assignment.vehicle_id,
                "start_date_time": str(assignment.start_date_time),
                "end_date_time": str(assignment.end_date_time) if assignment.end_date_time else None,
                "status": assignment.status
            } for assignment in assignments
        ]
        return jsonify(assignment_list), 200
    except Exception as e:
        logger.error(f"Error fetching assignments: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    
# Route to get a single assignment
@assignment_bp.route('/assignments/<int:assignment_id>', methods=['GET'])
def get_one_assignment(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404
        return jsonify(assignment.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching assignment: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


# Route to update a specific assignment
@assignment_bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        data = request.json
        assignment.driver_id = data.get('driver_id', assignment.driver_id)
        assignment.vehicle_id = data.get('vehicle_id', assignment.vehicle_id)
        assignment.start_date_time = data.get('start_date_time', assignment.start_date_time)
        assignment.end_date_time = data.get('end_date_time', assignment.end_date_time)
        assignment.status = data.get('status', assignment.status)

        db.session.commit()
        return jsonify({"message": "Assignment updated successfully", "assignment": assignment.to_dict()}), 200

    except Exception as e:
        logger.error(f"Error updating assignment: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


# Route to delete a specific assignment
@assignment_bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
        
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404

        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted successfully"}), 200

    except Exception as e:
        logger.error(f"Error deleting assignment: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500