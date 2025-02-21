from flask import Blueprint, request, jsonify, make_response

from app import app, db
from services import email_service

email_bp = Blueprint('email', __name__, url_prefix='/api/email')


@app.route('/api/email', methods=['POST'])
def add_email():
    data = request.get_json()
    
    if not data or not 'email' in data or not data['email']:
        return make_response(jsonify({'message': 'Email address is required!'}), 400)
    
    try:
        message, status_code = email_service.add_email(data['email'])
        return make_response(jsonify({'message': message}), status_code)
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new email! Please try again.'}), 500)
    

@app.route('/api/email', methods=['DELETE'])
def delete_email():
    data = request.get_json()
    
    if not data or not 'email' in data or not data['email']:
        return make_response(jsonify({'message': 'Email address is required!'}), 400)
    
    try:
        message, status_code = email_service.delete_email(data['email'])
        return make_response(jsonify({'message': message}), status_code)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting email! Please try again.'}), 500)
    

@app.route('/api/email/list', methods=['GET'])
def get_all_emails():
    try:
        emails, status_code = email_service.get_all_emails()
        return make_response(jsonify({'emails': emails}), status_code)
    except Exception as e:
        return make_response(jsonify({'message': 'Error retrieving emails! Please try again.'}), 500)
