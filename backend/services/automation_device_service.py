from flask import jsonify

from app import db
from models import AutomationDevice


def add_device(data):
    if not data or 'name' not in data or 'ip_address' not in data or not data['name'] or not data['ip_address']:
        return 'Device name and IP address are required!', 400 
    
    if AutomationDevice.query.filter_by(ip_address = data['ip_address']).first():
        return 'A device with the same IP address already exists!', 400

    new_device = AutomationDevice(
        name = data['name'], 
        ip_address = data['ip_address']
    )

    db.session.add(new_device)
    db.session.commit()

    return 'Device added successfully!', 201


def delete_device(device_id):
    try:
        device = AutomationDevice.query.get(device_id)
    
        if device:
            db.session.delete(device)
            db.session.commit()
            return True
        else:
            return False
        
    except Exception as e:
        return False
