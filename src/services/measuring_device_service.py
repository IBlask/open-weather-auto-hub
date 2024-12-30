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