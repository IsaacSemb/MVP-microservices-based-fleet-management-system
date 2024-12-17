from flask import Blueprint, request, jsonify
from services.service5_scheduling.models import Schedule
from common.database.db_utils import db
import os
import requests
from sqlalchemy.exc import SQLAlchemyError
from common.logs.logger import logger
from common.message_broker.rabbitmq_utils import RabbitMQ

broker = RabbitMQ()

SERVICE_7_URL = os.getenv('SERVICE_7_URL')
SERVICE_3_URL = os.getenv('SERVICE_3_URL')
SERVICE_4_URL = os.getenv('SERVICE_4_URL')

schedule_bp = Blueprint('schedule_bp', __name__)

# Route to create a new schedule
@schedule_bp.route('/schedules', methods=['POST'])
def create_schedule():
    
    try:
        data = request.json
        
        new_schedule = Schedule(
        schedule_type_id=data.get('schedule_type_id'),
        schedule_type=data.get('schedule_type'),
        start_date_time=data.get('start_date_time'), 
        end_date_time=data.get('end_date_time'),
        expected_completion=data.get('expected_completion'),
        status=data.get('status', 'scheduled'), 
        description=data.get('description')
        )

        db.session.add(new_schedule)
        db.session.commit()
        return jsonify({"message": "Schedule created successfully", "schedule_id": new_schedule.schedule_id}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error : {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        logger.error(f"An unexpected error occurred : {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500



# Route to get all schedules
@schedule_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    try:
        schedules = Schedule.query.all()
        
        if not schedules:
            return jsonify({"message": "No schedules found"}), 404
        
        schedule_list = [
            {
                "schedule_id": schedule.schedule_id,
                "schedule_type": schedule.schedule_type,
                "schedule_type_id": schedule.schedule_type_id,
                "start_date_time": str(schedule.start_date_time),
                "end_date_time": str(schedule.end_date_time),
                "expected_completion": str(schedule.expected_completion) if schedule.expected_completion else None,
                "status": schedule.status,
                "description": schedule.description
            } for schedule in schedules
        ]
        
        return jsonify(schedule_list), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error : {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        logger.error(f"An unexpected error occurred : {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    
    # USING BROKERS POSED A SKILL ISSUE LAMAO
    # SO WE SHALL USE APIS --- this is so problematic, it requires 3 services no no no no no
    for schedule in schedule_list:
        try:
            if schedule["schedule_type"] == "task":                
                response = requests.get(f"{SERVICE_7_URL}/tasks/{schedule['schedule_type_id']}", timeout=5)
                print(response.json())
                                
            elif schedule["schedule_type"] == "maintenance":
                response = requests.get(f"{SERVICE_4_URL}/maintenance/{schedule['schedule_type_id']}", timeout=5)
                print(response.json())                
            
            elif schedule["schedule_type"] == "assignment":
                response = requests.get(f"{SERVICE_3_URL}/assignments/{schedule['schedule_type_id']}", timeout=5)
                print(response.json())

            else:
                schedule["details"] = "Unknown schedule type"
                continue

            # Parse and add details
            if response.status_code == 200:
                schedule["details"] = response.json()
                
            else:
                schedule["details"] = f"Error: {response.status_code} - {response.text}"

        except requests.RequestException as e:
            schedule["details"] = f"Error fetching details: {str(e)}"

    return jsonify(schedule_list), 200









# Route to get a specific schedule
@schedule_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    
    try:
        schedule = Schedule.query.get(schedule_id)
        
        if not schedule:
            logger.error("Schedule not found")
            return jsonify({"error": "Schedule not found"}), 404
        
        schedule_data = {
            "schedule_id": schedule.schedule_id,
            "schedule_type_id": schedule.schedule_type_id,
            "schedule_type": schedule.schedule_type,
            "start_date_time": str(schedule.start_date_time),
            "end_date_time": str(schedule.end_date_time),
            "expected_completion": str(schedule.expected_completion) if schedule.expected_completion else None,
            "status": schedule.status,
            "description": schedule.description
        }
        return jsonify(schedule_data), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error : {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        logger.error(f"An unexpected error occurred : {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


# Route to update a specific schedule
@schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    try:
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404
        
        # Validate request JSON
        if not request.is_json:
            return jsonify({"error": "Request data must be in JSON format"}), 400
        
        data = request.json

        # Optional field updates
        schedule.schedule_type_id = data.get('schedule_type_id', schedule.schedule_type_id)
        schedule.schedule_type = data.get('schedule_type', schedule.schedule_type)
        schedule.start_date_time = data.get('start_date_time', schedule.start_date_time)
        schedule.end_date_time = data.get('end_date_time', schedule.end_date_time)
        schedule.expected_completion = data.get('expected_completion', schedule.expected_completion)
        schedule.status = data.get('status', schedule.status)
        schedule.description = data.get('description', schedule.description)
        
        db.session.commit()
        logger.info(f"[{schedule_id}] has been updated")
        return jsonify({"message": "Schedule updated successfully"}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error : {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        logger.error(f"An unexpected error occurred : {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


# Route to delete a specific schedule
@schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404
        
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({"message": "Schedule deleted successfully"}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error : {str(e)}")
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        logger.error(f"An unexpected error occurred : {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500