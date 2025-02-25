from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError

from app import app
from services import automation_request_service


automation_request_bp = Blueprint('automation_request', __name__, url_prefix='/api/automation-request')


@automation_request_bp.route('', methods=['POST'])
def add_request():
    try:
        data = request.get_json()
        
        message, status_code = automation_request_service.add_request(data)
        
        return make_response(jsonify({'message': message}), status_code)
    
    except IntegrityError as e:
        if hasattr(e.orig, 'pgcode') and e.orig.pgcode == '23503':  # Foreign key violation
            return make_response(jsonify({'message': 'No automation device found with that ID.'}), 500)
        else:
            return make_response(jsonify({'message': 'Database integrity error! Please try again.'}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new request! Please try again.'}), 500)