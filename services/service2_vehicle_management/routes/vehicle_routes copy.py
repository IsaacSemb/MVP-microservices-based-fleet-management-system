from flask import Blueprint, jsonify, request
from models import Vehicle
from db_init_config import db

vehicle_blueprint = Blueprint("vehicle_bp", __name__)

@vehicle_blueprint.route('/vehicles', methods=['POST'])
def register_vehicle():
    # get data into json form
    data = request.get_json()
    
    # manipulate
    new_vehicle = Vehicle(
        make = data["make"],
        model = data["model"],
        year = data["year"],
        reg_no = data["reg_no"],
        fuel_type = data["fuel_type"],
        vehicle_type=data['vehicle_type']
        )
    
    # write it to the db
    try:
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({"message": "Vehicle registered successfully!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
    

@vehicle_blueprint.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    # print(all_vehicles)
    vehicle_objects = [ vehicle.to_dict() for vehicle in all_vehicles ]
    
    # get vehicle summary
    # Calculate the total count of vehicles and types
    total_count = len(vehicle_objects)

    vehicle_type_counts = {}
    for vehicle in vehicle_objects:
        vehicle_type = vehicle['vehicle_type'].capitalize()
        vehicle_type_counts[vehicle_type] = vehicle_type_counts.get(vehicle_type, 0) + 1

    # Prepare the response
    response = {
        "summary": {
            "total_vehicles": total_count,
            "total_by_type": vehicle_type_counts
        },
        "details": vehicle_objects
    }
    # print(response)
    
    return jsonify(response), 200

    

@vehicle_blueprint.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    if vehicle:
       vehicle_object = vehicle.to_dict()
       return jsonify(vehicle_object),200
    else:
        return jsonify({"error": "vehicle not found"}), 404 
    

@vehicle_blueprint.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"message": "Vehicle deleted successfully"}), 200
    return jsonify({"error": "Vehicle not found"}), 404
    
    
    
    
@vehicle_blueprint.route('/vehicles/<vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    
    # search for id to see whether it exists
    vehicle = Vehicle.query.get(vehicle_id)
    
    # if it doesnt just stop there
    if not vehicle:
        return jsonify({"error": "vehicle not found"}), 404 
    
    # if it does get replacement data so that we can patch it up
    new_vehicle_data = request.get_json()
        
    # try patching for the existent ones, the one that dont exist, we use existing values
    vehicle.make = new_vehicle_data.get("make", vehicle.make)
    vehicle.model = new_vehicle_data.get("model", vehicle.model)
    vehicle.year = new_vehicle_data.get("year", vehicle.year)
    vehicle.reg_no = new_vehicle_data.get("reg_no", vehicle.reg_no)
    vehicle.fuel_type = new_vehicle_data.get("fuel_type", vehicle.fuel_type)
    vehicle.vehicle_type = new_vehicle_data.get("vehicle_type", vehicle.vehicle_type)
    
    # data.get( "field_name", existing_fall_back_value )
    
    # trying to commit it to database
    try:  
        db.session.commit()
        return jsonify({"message": "Vehicle updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400