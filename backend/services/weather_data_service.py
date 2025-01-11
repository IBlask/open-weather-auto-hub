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
    


def get_weather_data(filters):
    try:
        queries = []
        
        if not filters['type']:
            queries.append(Temperature.query)
            queries.append(Humidity.query)
            queries.append(Pressure.query)
            queries.append(Wind.query)
        elif filters['type'] == 'temperature':
            queries.append(Temperature.query)
        elif filters['type'] == 'humidity':
            queries.append(Humidity.query)
        elif filters['type'] == 'pressure':
            queries.append(Pressure.query)
        elif filters['type'] == 'wind':
            queries.append(Wind.query)
        else:
            return {'message': 'Invalid type provided!'}, 400

        if filters['measuring_device']:
            measuring_device = MeasuringDevice.query.filter_by(public_key=filters['measuring_device']).first()
            if not measuring_device:
                return {'message': 'Invalid measuring device key!'}, 400
            queries = [query.filter_by(measuring_device_id=measuring_device.id) for query in queries]

        if filters['start_time']:
            start_time = datetime.strptime(filters['start_time'], "%Y-%m-%d_%H:%M:%S")
            queries = [query.filter(query.column_descriptions[0]['type'].created_at >= start_time) for query in queries]

        if filters['end_time']:
            end_time = datetime.strptime(filters['end_time'], "%Y-%m-%d_%H:%M:%S")
            queries = [query.filter(query.column_descriptions[0]['type'].created_at <= end_time) for query in queries]

        if filters['last_n']:
            queries = [query.order_by(query.column_descriptions[0]['type'].created_at.desc()).limit(int(filters['last_n'])) for query in queries]

        
        results = [query.all() for query in queries]
        data = []
        for result in results:
            data.append([res.to_dict() for res in result])
        
        
        if filters['type']:
            return {
                filters['type']: data[0]
            }, 200
        else:
            return {
                'temperature': data[0], 
                'humidity': data[1], 
                'pressure': data[2], 
                'wind': data[3]
                }, 200

    except Exception as e:
        return {'message': 'Error retrieving weather data! Please try again.'}, 500