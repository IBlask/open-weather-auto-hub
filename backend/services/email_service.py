from flask import jsonify
from sqlalchemy.exc import IntegrityError

from app import db
from models import Email


def add_email(email_address):
    if not email_address or email_address.isspace():
        return 'Email address is required!', 400
    
    try:
        email = Email(email = email_address)
        db.session.add(email)
        db.session.commit()
        return 'Email added successfully!', 200
    except IntegrityError:
        return 'Email address already exists!', 400
    except Exception as e:
        return 'Error adding new email! Please try again.', 500


def delete_email(email_address):
    if not email_address or email_address.isspace():
        return 'Email address is required!', 400

    try:
        email = Email.query.get(email_address)
        if email:
            db.session.delete(email)
            db.session.commit()
            return 'Email deleted successfully!', 200
        return 'Email address not found!', 404
    except Exception as e:
        return 'Error deleting email! Please try again.', 500