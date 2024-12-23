from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from services.service6_fuel_consumption_service.models.fuel_consumption_model import FuelConsumption, db
from common.logs.logger import logger
from common.message_broker.rabbitmq_utils import RabbitMQ


fuel_consumption_bp = Blueprint('fuel_consumption_bp', __name__)




# Helper function for validating request data
def validate_fuel_data(data, is_update=False):
    required_fields = ['vehicle_id', 'date', 'fuel_type', 'amount', 'cost']
    if not is_update:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    if not is_update:
        try:
            float(data.get('amount', 0))
            float(data.get('cost', 0))
        except ValueError:
            return False, "Amount and cost must be numeric values."
    return True, None


# Route to add a new fuel record
@fuel_consumption_bp.route('/fuel', methods=['POST'])
def add_fuel_record():
    
    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400

    is_valid, error_message = validate_fuel_data(data)
    
    if not is_valid:
        return jsonify({"error": error_message}), 400

    try:
        new_fuel_record = FuelConsumption(
            vehicle_id=data['vehicle_id'],
            date=data['date'],
            fuel_type=data['fuel_type'],
            amount=data['amount'],
            cost=data['cost'],
            mileage=data.get('mileage')
        )
        db.session.add(new_fuel_record)
        db.session.commit()
        logger.info(f"new fuel log added to db: ID:{new_fuel_record.fuel_id}")
        
        try:
            # Publish to the broker
            new_fuel_record_created_message = {
                "event_type": "fuel_created",
                "data": new_fuel_record.to_dict()
            }
            
            # get broker
            broker = RabbitMQ()
            broker.publish_message(
                exchange='fuel_record_fanout_exchange',
                exchange_type='fanout',
                routing_key='',
                message=new_fuel_record_created_message
            )
            logger.info(f"published new fuel record: {new_fuel_record.fuel_id}")
        except Exception as e:
            # Log broker error
            logger.error(f"Error publishing message to broker: {str(e)}")
            return jsonify({"message": "fuel record created but failed to notify listeners", "fuel record": new_fuel_record.to_dict()}), 201

        
        
        return jsonify({"message": "Fuel record added successfully"}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error creating fuel record: {str(e)}")        
        return jsonify({"error": f"Database error: {str(e)}"}), 500








# Route to get all fuel records
@fuel_consumption_bp.route('/fuel', methods=['GET'])
def get_fuel_records():
    try:
        records = FuelConsumption.query.all()
        if not records:
            return jsonify({"message": "No fuel records found"}), 200

        fuel_list = [
            {
                "fuel_id": record.fuel_id,
                "vehicle_id": record.vehicle_id,
                "date": str(record.date),
                "fuel_type": record.fuel_type,
                "amount": record.amount,
                "cost": record.cost,
                "mileage": record.mileage
            } for record in records
        ]
        return jsonify(fuel_list), 200
    except SQLAlchemyError as e:
        logger.error(f"Database Error : {str(e)}")        
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Route to get a specific fuel record
@fuel_consumption_bp.route('/fuel/<int:fuel_id>', methods=['GET'])
def get_fuel_record(fuel_id):
    try:
        record = FuelConsumption.query.get(fuel_id)
        if not record:
            return jsonify({"error": "Fuel record not found"}), 404

        fuel_data = {
            "fuel_id": record.fuel_id,
            "vehicle_id": record.vehicle_id,
            "date": str(record.date),
            "fuel_type": record.fuel_type,
            "amount": record.amount,
            "cost": record.cost,
            "mileage": record.mileage
        }
        return jsonify(fuel_data), 200
    except SQLAlchemyError as e:
        logger.error(f"Database Error : {str(e)}")        
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Route to update a specific fuel record
@fuel_consumption_bp.route('/fuel/<int:fuel_id>', methods=['PUT'])
def update_fuel_record(fuel_id):
    record = FuelConsumption.query.get(fuel_id)
    if not record:
        return jsonify({"error": "Fuel record not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400

    is_valid, error_message = validate_fuel_data(data, is_update=True)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    try:
        record.vehicle_id = data.get('vehicle_id', record.vehicle_id)
        record.date = data.get('date', record.date)
        record.fuel_type = data.get('fuel_type', record.fuel_type)
        record.amount = data.get('amount', record.amount)
        record.cost = data.get('cost', record.cost)
        record.mileage = data.get('mileage', record.mileage)

        db.session.commit()
        return jsonify({"message": "Fuel record updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database Error : {str(e)}")        
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# Route to delete a specific fuel record
@fuel_consumption_bp.route('/fuel/<int:fuel_id>', methods=['DELETE'])
def delete_fuel_record(fuel_id):
    try:
        record = FuelConsumption.query.get(fuel_id)
        if not record:
            return jsonify({"error": "Fuel record not found"}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Fuel record deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database Error : {str(e)}")        
        return jsonify({"error": f"Database error: {str(e)}"}), 500
