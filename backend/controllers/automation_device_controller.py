from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError, DataError

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


@automation_device_bp.route('/list', methods=['GET'])
def list_devices():
    try:
        devices = automation_device_service.get_all_devices()
        
        device_list = [{'id': device.id, 'name': device.name, 'ip_address': device.ip_address} for device in devices]
        
        return jsonify(device_list), 200
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error retrieving devices! Please try again.'}), 500)

@automation_device_bp.route('/<device_id>', methods=['GET'])
def get_device(device_id):
    try:
        device = automation_device_service.get_device(device_id)
        
        if device:
            return jsonify({'id': device.id, 'name': device.name, 'ip_address': device.ip_address}), 200
        else:
            return make_response(jsonify({'message': 'Device not found!'}), 404)
    
    except IntegrityError as e:
        return make_response(jsonify({'message': 'Database integrity error! Please try again.'}), 500)
    except DataError as e:
        if 'InvalidTextRepresentation' in str(e):
            return make_response(jsonify({'message': 'Invalid device ID!'}), 400)
        return make_response(jsonify({'message': 'Data error! Please try again.'}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting request! Please try again.'}), 500)
