from flask import Blueprint, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ

from app import app
from services import measuring_device_service


measuring_device_bp = Blueprint('measuring_device', __name__, url_prefix='/api/measuring-device')


@measuring_device_bp.route('/add', methods=['POST'])
def add_device():
    try:
        data = request.get_json()
        
        return_data = measuring_device_service.add_device(data)
        
        return return_data, 201
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new device! Please try again.'}), 500)