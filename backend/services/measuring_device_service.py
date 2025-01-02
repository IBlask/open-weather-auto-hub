from flask import jsonify

from app import db
from models import MeasuringDevice


def add_device(data):
    new_device = MeasuringDevice(name = data['name'])

    db.session.add(new_device)
    db.session.commit()

    return jsonify({
        'name': new_device.name,
        'public-key': new_device.public_key
    })


def delete_device(device_id):
    try:
        device = MeasuringDevice.query.get(device_id)
    
        if device:
            db.session.delete(device)
            db.session.commit()
            return True
        else:
            return False
        
    except Exception as e:
        return False


def get_all_devices():
    devices = MeasuringDevice.query.all()
    return devices