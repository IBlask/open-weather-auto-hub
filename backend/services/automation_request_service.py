from flask import json, jsonify
import requests
import logging

from app import db
from models import AutomationRequest, AutomationDevice


def add_request(data):
    if not data or 'device_id' not in data or 'name' not in data or not data['device_id'] or not data['name']:
        return 'Device ID and request name are required!', 400
    if 'trigger' not in data or 'trigger_value' not in data or not data['trigger'] or not data['trigger_value'] or 'trigger_operator' not in data or not data['trigger_operator']:
        return 'Trigger type, value and operator are required!', 400
    
    if data['trigger'] not in ['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_direction', 'rain_prediction']:
        return 'Invalid trigger type! Must be one of: temperature, humidity, pressure, wind_speed, wind_direction, rain_prediction', 400
    if data['trigger_operator'] not in ['<', '>', '<=', '>=', '==', '!=']:
        return 'Invalid trigger operator! Must be one of: <, >, <=, >=, ==, !=', 400
    
    data['trigger_value'] = float(data['trigger_value'])
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
        new_request.port = int(data['port'])
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


def get_all_requests():
    try:
        requests = AutomationRequest.query.all()
        return [{'id': request.id, 
                 'device_id': request.automation_device_id, 
                 'name': request.name, 
                 'trigger': request.trigger, 
                 'trigger_value': request.trigger_value, 
                 'trigger_operator': request.trigger_operator, 
                 'port': request.port, 
                 'uri': request.uri, 
                 'body': request.body} 
                for request in requests]
    
    except Exception as e:
        raise e
    

def send_http_request(automation_request):
    try:
        # Query the database to get the IP address of the automation device
        device = AutomationDevice.query.get(automation_request.automation_device_id)
        if not device:
            raise ValueError("Automation device not found!")

        # Construct the URL
        url = f"http://{device.ip_address}"
        if automation_request.port:
            url += f":{automation_request.port}"
        if automation_request.uri:
            if automation_request.uri[0] != '/':
                url += "/"
            url += f"{automation_request.uri}"

        # Set the body of the HTTP request
        try:
            body = json.loads(automation_request.body) if automation_request.body else {}
        except json.JSONDecodeError:
            body = {}
        
        # Send the HTTP request
        response = requests.post(url, json=body)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        # Log the error details
        logging.error(f"HTTP request failed: {e.response.status_code} {e.response.reason} for url: {e.response.url}")
        logging.error(f"Response content: {e.response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")

    except Exception as e:
        logging.error(f"Error sending HTTP request: {e}")


def is_request_triggered(request, value):
    trigger_operator = request.trigger_operator
    trigger_value = float(request.trigger_value)
    value = float(value)

    if trigger_operator == '<' and value < trigger_value:
        return 1
    elif trigger_operator == '>' and value > trigger_value:
        return 1
    elif trigger_operator == '<=' and value <= trigger_value:
        return 1
    elif trigger_operator == '>=' and value >= trigger_value:
        return 1
    elif trigger_operator == '==' and value == trigger_value:
        return 1
    elif trigger_operator == '!=' and value != trigger_value:
        return 1
