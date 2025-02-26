from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError, DataError

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
    except DataError as e:
        if 'InvalidTextRepresentation' in str(e):
            return make_response(jsonify({'message': 'Invalid device ID!'}), 400)
        return make_response(jsonify({'message': 'Data error! Please try again.'}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'Error adding new request! Please try again.'}), 500)
    

@automation_request_bp.route('/<request_id>', methods=['DELETE'])
def delete_request(request_id):
    try:
        if automation_request_service.delete_request(request_id):
            return make_response(jsonify({'message': 'Request deleted successfully!'}), 200)
        else:
            return make_response(jsonify({'message': 'Request ID not found!'}), 404)
    
    except IntegrityError as e:
        return make_response(jsonify({'message': 'Database integrity error! Please try again.'}), 500)
    except DataError as e:
        if 'InvalidTextRepresentation' in str(e):
            return make_response(jsonify({'message': 'Invalid request ID!'}), 400)
        return make_response(jsonify({'message': 'Data error! Please try again.'}), 500)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting request! Please try again.'}), 500)


@automation_request_bp.route('/list', methods=['GET'])
def get_all_requests():
    try:
        requests = automation_request_service.get_all_requests()
        
        return make_response(jsonify(requests), 200)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error fetching requests! Please try again.'}), 500)
