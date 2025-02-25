from flask import Blueprint, request, jsonify, make_response

from app import app
from services import automation_request_service


automation_request_bp = Blueprint('automation_request', __name__, url_prefix='/api/automation-request')


@automation_request_bp.route('', methods=['POST'])
def add_request():
    try:
        data = request.get_json()
        
        message, status_code = automation_request_service.add_request(data)
        
        return make_response(jsonify({'message': message}), status_code)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new request! Please try again.' + str(e)}), 500)
