from flask import Blueprint, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ

from app import app
from services import measuring_device_service


measuring_device_bp = Blueprint('measuring_device', __name__, url_prefix='/api/measuring-device')


@measuring_device_bp.route('/', methods=['POST'])
def add_device():
    try:
        data = request.get_json()
        
        return_data = measuring_device_service.add_device(data)
        
        return return_data, 201
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new device! Please try again.'}), 500)
    


@measuring_device_bp.route('/', methods=['DELETE'])
def delete_device():
    try:
        if not request.data:
            return make_response(jsonify({'message': 'No data provided!'}), 400)

        data = request.get_json()
        device_id = data.get('device_id')
        
        if not device_id:
            return make_response(jsonify({'message': 'Device ID is required!'}), 400)
        
        result = measuring_device_service.delete_device(device_id)
        
        if result:
            return make_response(jsonify({'message': 'Device deleted successfully!'}), 200)
        else:
            return make_response(jsonify({'message': 'Device not found!'}), 404)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting device! Please try again.'}), 500)



@measuring_device_bp.route('/list', methods=['GET'])
def list_devices():
    try:
        devices = measuring_device_service.get_all_devices()
        
        device_list = [{'id': device.id, 'name': device.name, 'public_key': device.public_key} for device in devices]
        
        return jsonify(device_list), 200
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error retrieving devices! Please try again.'}), 500)