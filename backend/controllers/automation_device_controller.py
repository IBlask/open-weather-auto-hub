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


@automation_device_bp.route('', methods=['DELETE'])
def delete_device():
    try:
        data = request.get_json()
        
        if not data or 'device_id' not in data or not data['device_id']:
            return make_response(jsonify({'message': 'Device ID is required!'}), 400)
        
        result = automation_device_service.delete_device(data['device_id'])
        
        if result:
            return make_response(jsonify({'message': 'Device deleted successfully!'}), 200)
        else:
            return make_response(jsonify({'message': 'Device not found!'}), 404)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting device! Please try again.'}), 500)
