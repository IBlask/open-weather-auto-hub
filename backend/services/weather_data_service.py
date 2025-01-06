from datetime import datetime

from app import db
from models import Temperature, Humidity, Pressure, Wind, MeasuringDevice


def save_weather_data(data):
    try:
        measuring_device_key = data.get('measuring_device')
        measuring_device = MeasuringDevice.query.filter_by(public_key = measuring_device_key).first()

        if not measuring_device:
            return 'Invalid measuring device key!', 400
        
        measuring_device_id = measuring_device.id
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'temperature' in data and data['temperature'].strip():
            temperature = Temperature(
                value = data['temperature'],
                measuring_device_id = measuring_device_id,
                created_at = created_at
            )
            db.session.add(temperature)

        if 'humidity' in data and data['humidity'].strip():
            humidity = Humidity(
                value = data['humidity'],
                measuring_device_id = measuring_device_id,
                created_at = created_at
            )
            db.session.add(humidity)

        if 'pressure' in data and data['pressure'].strip():
            pressure = Pressure(
                value = data['pressure'],
                measuring_device_id = measuring_device_id,
                created_at = created_at
            )
            db.session.add(pressure)

        if ('wind_speed' in data and 'wind_direction' in data 
            and data['wind_speed'].strip() and data['wind_direction'].strip()):
            wind = Wind(
                speed = data['wind_speed'],
                direction = data['wind_direction'],
                measuring_device_id = measuring_device_id,
                created_at = created_at
            )
            db.session.add(wind)

        db.session.commit()

        return 'Weather data saved successfully!', 201

    except Exception as e:
        return 'Error saving weather data! Please try again.', 500