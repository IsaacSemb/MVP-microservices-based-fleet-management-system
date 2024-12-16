from flask import Blueprint, request, jsonify, current_app
from models import MaintenanceLog
from shared.database.db_utils import db
from functools import wraps
from shared.message_broker.rabbitmq_utils import RabbitMQ


broker = RabbitMQ()

maintenance_logs_bp = Blueprint('maintenance_logs_bp', __name__)


def check_my_db(func):
    """ this check for whether the database is available at the moment or not"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config.get('DB_AVAILABLE', True):
            return jsonify({"message": "Service unavailable due to database issues. Please try again later."}), 503
        return func(*args, **kwargs)
    return wrapper


# Route to add a new maintenance log
@maintenance_logs_bp.route('/maintenance', methods=['POST'])
@check_my_db
def add_maintenance_log():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid request. JSON data is required."}), 400
        
        new_log = MaintenanceLog(
            vehicle_id=data.get('vehicle_id'),
            maintenance_type=data.get('maintenance_type', 'unspecified'),
            start_date_time=data.get('start_date_time'),
            cost=data.get('cost'),
            description=data.get('description'),
            parts_used=data.get('parts_used'),
            expected_completion_date_time=data.get('expected_completion_date_time'),
            status=data.get('status', 'scheduled')
        )
        db.session.add(new_log)
        db.session.commit()

        # Publish to the broker
        new_maintenance_created_message = {
            "event_type": "maintenance_created",
            "data": new_log.to_dict()
        }
        
        try:
            
            """   
            considerations made ... 
            should we write to db even when broker fails
            because then the schedule data will be inconsistent 
            we can do a transational outbox ie when data fails we have a table that logs it in the db
            we frequently check this table to retry sending the messages to the broker again
            we can implement this later for now let us risk inconsistency
            originally i planned to cross query maintence adn schedule for records (based on ID and dates i think)
            to see which ones the maintenance has that arent in the scheduler, we can then resend those ones !!!!!!
            """
            
            broker.publish_message(
                exchange='maintenance_created_direct_exchange', 
                exchange_type='direct',
                routing_key='maintenance.created',
                message=new_maintenance_created_message
            )
            
        except Exception as broker_error:
            # Log the error and proceed without breaking the flow
            current_app.logger.error(f"Broker publishing error: {broker_error}")
            return jsonify({
                "message": "Maintenance log added successfully, but failed to notify via broker.",
                "broker_error": str(broker_error)
            }), 201

        return jsonify({"message": "Maintenance log added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while adding the maintenance log: {str(e)}"}), 500


# Route to get all maintenance logs
@maintenance_logs_bp.route('/maintenance', methods=['GET'])
@check_my_db
def get_maintenance_logs():
    try:
        logs = MaintenanceLog.query.all()
        maintenance_list = [ log.to_dict() for log in logs]
        
        return jsonify(maintenance_list), 200
    
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching maintenance logs: {str(e)}"}), 500


# Route to get a specific maintenance log
@maintenance_logs_bp.route('/maintenance/<int:maintenance_id>', methods=['GET'])
@check_my_db
def get_maintenance_log(maintenance_id):
    try:
        log = MaintenanceLog.query.get(maintenance_id)
        
        if log:
            log_data = log.to_dict() 
                
            return jsonify(log_data), 200
        else:
            return jsonify({"error": "Maintenance log not found"}), 404
        
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching the maintenance log: {str(e)}"}), 500
    

# Route to update a specific maintenance log
@maintenance_logs_bp.route('/maintenance/<int:maintenance_id>', methods=['PUT'])
@check_my_db
def update_maintenance_log(maintenance_id):
    try:
        log = MaintenanceLog.query.get(maintenance_id)
        if not log:
            return jsonify({"error": "Maintenance log not found"}), 404

        data = request.json
        log.vehicle_id = data.get('vehicle_id', log.vehicle_id)
        log.maintenance_type = data.get('maintenance_type', log.maintenance_type)
        log.start_date_time = data.get('start_date_time', log.start_date_time)
        log.end_date_time = data.get('end_date_time', log.end_date_time)
        log.expected_completion_date_time = data.get('expected_completion_date_time', log.expected_completion_date_time)
        log.cost = data.get('cost', log.cost)
        log.description = data.get('description', log.description)
        log.parts_used = data.get('parts_used', log.parts_used)
        log.status = data.get('status', log.status)

        db.session.commit()
        return jsonify({"message": "Maintenance log updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while updating the maintenance log: {str(e)}"}), 500


# Route to delete a specific maintenance log
@maintenance_logs_bp.route('/maintenance/<int:maintenance_id>', methods=['DELETE'])
@check_my_db
def delete_maintenance_log(maintenance_id):
    try:
        log = MaintenanceLog.query.get(maintenance_id)
        if not log:
            return jsonify({"error": "Maintenance log not found"}), 404

        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Maintenance log deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while deleting the maintenance log: {str(e)}"}), 500