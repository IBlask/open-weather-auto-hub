from flask import Blueprint, request, jsonify, make_response

from services import weather_data_service


weather_data_bp = Blueprint('weather_data', __name__, url_prefix='/api/weather-data')


@weather_data_bp.route('/', methods=['POST'])
def save_weather_data():
    try:
        if not request.data:
            return make_response(jsonify({'message': 'No data provided!'}), 400)
        
        data = request.get_json()

        if (not data
            or 'measuring_device' not in data
            or ("temperature" not in data 
                 and "humidity" not in data 
                 and "pressure" not in data 
                 and ("wind_speed" not in data and "wind_direction" not in data))):

            return make_response(jsonify({'message': 'Invalid data provided!'}), 400)

        message, status_code = weather_data_service.save_weather_data(data)
        
        return make_response(jsonify({'message': message}), status_code)
    
    except Exception as e:
        return make_response(jsonify({'message': 'Error saving weather data! Please try again.'}), 500)