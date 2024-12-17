
from functools import wraps
from flask import jsonify


def check_my_db(func, current_app):
    """ this check for whether the database is available at the moment or not"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config.get('DB_AVAILABLE', True):
            return jsonify({"message": "Service unavailable due to database issues. Please try again later."}), 503
        return func(*args, **kwargs)
    return wrapper