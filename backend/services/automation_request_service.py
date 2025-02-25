from flask import jsonify

from app import db
from models import AutomationRequest


def add_request(data):
    if not data or 'device_id' not in data or 'name' not in data or not data['device_id'] or not data['name']:
        return 'Device ID and request name are required!', 400
    
    new_request = AutomationRequest(
        automation_device_id = data['device_id'], 
        name = data['name']
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