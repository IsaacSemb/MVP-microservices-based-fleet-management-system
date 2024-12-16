
from flask import Blueprint, jsonify, request
from models import Task
from shared.database.db_utils import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from shared.message_broker.rabbitmq_utils import RabbitMQ

broker = RabbitMQ()




# Creation of the blueprint for routing
task_blueprint = Blueprint("task_bp", __name__)

# Create a new task
@task_blueprint.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        new_task = Task(
            task=data["task"],
            assignment_id=data["assignment_id"],
            start_date_time=data.get("start_date_time", datetime.now(timezone.utc)),
            expected_completion_date_time=data.get("expected_completion_date_time"),
            end_date_time=data.get("end_date_time"),
            description=data.get("description"),
            priority=data.get("priority", "low"), 
            status=data.get("status", "scheduled")
        )

        db.session.add(new_task)
        db.session.commit()
        
        
        # Publish to the broker
        new_task_created_message = {
            "event_type": "task_created",
            "data": new_task.to_dict()
        }
        
        #  using fanout to correct the issue
        broker.publish_message(
            exchange='task_created_direct_exchange', 
            exchange_type='direct',
            routing_key='task.created',  # in fanouts, there is not routing key
            message=new_task_created_message
            )
        
        
        return jsonify({"message": "Task created successfully!", "task": new_task.to_dict()}), 201

    except KeyError as e:
        db.session.rollback()
        missing_field = str(e).strip("'")
        print(f"Missing field: {missing_field}")
        return jsonify({"error": f"Missing required field: {missing_field}"}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({"error": "An error occurred while saving the task to the database. Please try again."}), 500

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


# Get all tasks
@task_blueprint.route('/tasks', methods=['GET'])
def get_all_tasks():
    try:
        all_tasks = Task.query.all()
        task_objects = [task.to_dict() for task in all_tasks]
        return jsonify(task_objects), 200

    except SQLAlchemyError as e:
        print(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching tasks. Please try again later."}), 500

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


# Get a single task by ID
@task_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task:
            return jsonify(task.to_dict()), 200
        else:
            return jsonify({"error": "Task not found"}), 404

    except SQLAlchemyError as e:
        print(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while fetching the task. Please try again later."}), 500

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


# Delete a task by ID
@task_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted successfully"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the task. Please try again later."}), 500

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


# Update a task by ID
@task_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Update task fields
        task.task = data.get("task", task.task)
        task.assignment_id = data.get("assignment_id", task.assignment_id)
        task.start_date_time = data.get("start_date_time", task.start_date_time)
        task.expected_completion_date_time = data.get("expected_completion_date_time", task.expected_completion_date_time)
        task.end_date_time = data.get("end_date_time", task.end_date_time)
        task.description = data.get("description", task.description)
        task.priority = data.get("priority", task.priority)
        task.status = data.get("status", task.status)

        db.session.commit()
        return jsonify({"message": "Task updated successfully!", "task": task.to_dict()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while updating the task. Please try again later."}), 500

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
