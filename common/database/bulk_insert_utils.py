from sqlalchemy.exc import SQLAlchemyError
from db_init_config import db

# General-purpose bulk insert function
def bulk_insert(model, data_list):
    """
    Insert multiple entries into the database using SQLAlchemy bulk_insert_mappings.
    model (db.Model): The SQLAlchemy model class to insert data into.
    data_list (list): A list of dictionaries representing the rows to insert.
    """
    try:
        # Using bulk_insert_mappings to insert multiple records
        db.session.bulk_insert_mappings(model, data_list)
        db.session.commit()
        print(f"Data successfully inserted into {model.__tablename__} table.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error occurred: {e}")

