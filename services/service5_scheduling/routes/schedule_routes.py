from flask import Blueprint, request, jsonify
from models import Schedule
from shared.database.db_utils import db
import os
import requests

from shared.message_broker.rabbitmq_utils import RabbitMQ

broker = RabbitMQ()

SERVICE_7_URL = os.getenv('SERVICE_7_URL')
SERVICE_3_URL = os.getenv('SERVICE_3_URL')
SERVICE_4_URL = os.getenv('SERVICE_4_URL')

schedule_bp = Blueprint('schedule_bp', __name__)

# Route to create a new schedule
@schedule_bp.route('/schedules', methods=['POST'])
def create_schedule():
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
    return jsonify({"message": "Schedule created successfully"}), 201


# Route to get all schedules
@schedule_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    schedules = Schedule.query.all()
    
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
    
    notes = """    
    this service contains threee other service data    
    tasks
    assignments
    maitenances    
    we need details from those services when sending them over to whoever asked for them    
    """
    print(schedule_list)
    # USING BROKERS POSED A SKILL ISSUE LAMAO
    # SO WE SHALL USE APIS
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
    schedule = Schedule.query.get(schedule_id)
    if schedule:
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
    else:
        return jsonify({"error": "Schedule not found"}), 404

# Route to update a specific schedule
@schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({"error": "Schedule not found"}), 404

    data = request.json
    
    # schedule.schedule_type_id = data.get('schedule_type_id', schedule.schedule_type_id) 
    schedule.schedule_type = data.get('schedule_type', schedule.schedule_type)
    schedule.start_date_time = data.get('start_date_time', schedule.start_date_time) 
    schedule.end_date_time = data.get('end_date_time', schedule.end_date_time)  
    schedule.expected_completion = data.get('expected_completion', schedule.expected_completion)  
    schedule.status = data.get('status', schedule.status)
    schedule.description = data.get('description', schedule.description)

    db.session.commit()
    return jsonify({"message": "Schedule updated successfully"}), 200

# Route to delete a specific schedule
@schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({"error": "Schedule not found"}), 404

    db.session.delete(schedule)
    db.session.commit()
    return jsonify({"message": "Schedule deleted successfully"}), 200
