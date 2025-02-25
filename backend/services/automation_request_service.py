from flask import jsonify

from app import db
from models import AutomationRequest


def add_request(data):
    if not data or 'device_id' not in data or 'name' not in data or not data['device_id'] or not data['name']:
        return 'Device ID and request name are required!', 400
    if 'trigger' not in data or 'trigger_value' not in data or not data['trigger'] or not data['trigger_value'] or 'trigger_operator' not in data or not data['trigger_operator']:
        return 'Trigger type, value and operator are required!', 400
    
    if data['trigger'] not in ['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_direction', 'rain_prediction']:
        return 'Invalid trigger type! Must be one of: temperature, humidity, pressure, wind_speed, wind_direction, rain_prediction', 400
    if data['trigger_operator'] not in ['<', '>', '<=', '>=', '==', '!=']:
        return 'Invalid trigger operator! Must be one of: <, >, <=, >=, ==, !=', 400
    if data['trigger'] == 'rain_prediction' and (data['trigger_value'] < 0 or data['trigger_value'] > 1):
        return 'Rain prediction value must be between 0 and 1!', 400
    if data['trigger'] == 'wind_direction' and (data['trigger_value'] < 0 or data['trigger_value'] > 360):
        return 'Wind direction value must be between 0 and 360!', 400
    if data['trigger'] == 'humidity' and (data['trigger_value'] < 0 or data['trigger_value'] > 100):
        return 'Humidity value must be between 0 and 100!', 400
    
    new_request = AutomationRequest(
        automation_device_id = data['device_id'], 
        name = data['name'],
        trigger = data['trigger'],
        trigger_value = data['trigger_value'],
        trigger_operator = data['trigger_operator']
    )

    if 'port' in data and data['port']:
        new_request.port = data['port']
    if 'uri' in data and data['uri']:
        new_request.uri = data['uri']
    if 'body' in data and data['body']:
        new_request.body = data['body']

    db.session.add(new_request)
    db.session.commit()

    return 'Request added successfully!', 201


def delete_request(request_id):
    try:
        request = AutomationRequest.query.get(request_id)
    
        if request:
            db.session.delete(request)
            db.session.commit()
            return True
        else:
            return False
        
    except Exception as e:
        raise e
