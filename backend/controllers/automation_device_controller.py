from flask import Blueprint, request, jsonify, make_response

from app import app
from services import automation_device_service


automation_device_bp = Blueprint('automation_device', __name__, url_prefix='/api/automation-device')


@automation_device_bp.route('', methods=['POST'])
def add_device():
    try:
        data = request.get_json()
        
        message, status_code = automation_device_service.add_device(data)
        
        return make_response(jsonify({'message': message}), status_code)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new device! Please try again.'}), 500)
