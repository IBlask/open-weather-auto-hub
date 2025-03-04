from datetime import datetime, timedelta

from app import db
from models import Temperature, Humidity, Pressure, Wind, RainPrediction, MeasuringDevice, AutomationRequest
from services import automation_request_service

# INFLUENCE OF PARAMETERS IN PREDICTION
PRESSURE_ABS_SHARE = 0.2                # absoulte pressure value -> 1010 hPa 
PRESSURE_DELTA_SHARE = 0.15             # pressure change over time: x -> 1010 hPa
HUMIDITY_ABS_SHARE = 0.15               # absolute humidity value -> 100%
HUMIDITY_DELTA_SHARE = 0.1              # humidity change over time: x -> 100%
WIND_SPEED_SHARE = 0.05                 # wind speed -> 15 km/h
WIND_DIRECTION_DELTA_SHARE = 0.2        # wind direction -> 220 degrees
WIND_DIRECTION_CHANGE_SHARE = 0.05      # wind direction change over time: x -> 220 degrees
TEMPERATURE_ABS_SHARE = 0.05            # temperature -> 5-20 degrees celsius
TEMPERATURE_DELTA_SHARE = 0.05          # temperature change over time: x -> 5-20 degrees celsius

# VARIABLES FOR SEA LEVEL PRESSURE CALCULATION
L = 0.0065      # K/m (temperature gradient)
T0 = 288.15     # K (standard temperature at sea level)
g = 9.80665     # m/s^2 (gravitational acceleration)
M = 0.0289644   # kg/mol (molar mass of air)
R = 8.31432     # J/(mol*K) (gas constant)


def get_data():
    timeframe_min = datetime.now() - timedelta(hours = 1)

    temperature = Temperature.query.filter(Temperature.created_at >= timeframe_min).all()
    humidity = Humidity.query.filter(Humidity.created_at >= timeframe_min).all()
    pressure = Pressure.query.filter(Pressure.created_at >= timeframe_min).all()
    wind = Wind.query.filter(Wind.created_at >= timeframe_min).all()

    sea_level_pressure = []
    for p in pressure:
        measuring_device = MeasuringDevice.query.get(p.measuring_device_id)
        new_pressure_value = p.value * (1 + (L * measuring_device.altitude) / T0) ** (g * M / (R * L))
        new_pressure = Pressure(value = new_pressure_value, measuring_device_id = p.measuring_device_id, created_at = p.created_at)
        sea_level_pressure.append(new_pressure)

    return {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': sea_level_pressure,
        'wind': wind
    }


def predict_rain():
    data = get_data()
    
    if not data['humidity'] or not data['pressure']:
        raise ValueError('Insufficient data to predict rain!')

    if data['humidity'][-1].value > 90 and data['pressure'][-1].value < 1010:
        prediction = 1
    else:
        prediction = 0

        pressure_delta = 1 - ((data['pressure'][-1].value - 1010) / 5)
        pressure_change = data['pressure'][-1].value - data['pressure'][0].value
        pressure_change_time = data['pressure'][-1].created_at - data['pressure'][0].created_at
        pressure_change_time_seconds = pressure_change_time.total_seconds()

        # Add a small epsilon value to avoid division by zero or near-zero values
        epsilon = 1e-6
        if pressure_change_time_seconds > epsilon:
            pressure_change_delta = pressure_change / (pressure_change_time_seconds / 60) * 60
        else:
            pressure_change_delta = 0

        humidity_delta = data['humidity'][-1].value - data['humidity'][0].value

        wind_speed_mean = sum([wind.speed for wind in data['wind']]) / len(data['wind'])
        wind_direction_norm_first = data['wind'][0].direction if data['wind'][0].direction - 40 >= 0 else 360 - (40 - data['wind'][0].direction)
        wind_direction_norm_last = data['wind'][-1].direction if data['wind'][-1].direction - 40 >= 0 else 360 - (40 - data['wind'][-1].direction)
        wind_direction_delta = abs(180 - wind_direction_norm_last)
        wind_direction_change_delta = abs(180 - wind_direction_norm_first) - abs(180 - wind_direction_norm_last)

        temperature_delta =  abs(13 - data['temperature'][-1].value)
        temperature_change_delta = abs(13 - data['temperature'][0].value) - abs(13 - data['temperature'][-1].value)


        if (data['pressure'][-1].value <= 1010): 
            prediction += PRESSURE_ABS_SHARE
        elif (data['pressure'][-1].value <= 1015):
            prediction += PRESSURE_ABS_SHARE * pressure_delta
        
        if (pressure_change_delta >= 2):
            prediction += PRESSURE_DELTA_SHARE
        elif (pressure_change_delta >= 0):
            prediction += PRESSURE_DELTA_SHARE * (pressure_change_delta / 2)

        prediction += data['humidity'][-1].value / 100 * HUMIDITY_ABS_SHARE  
        
        if (humidity_delta > 0):
            prediction += HUMIDITY_DELTA_SHARE * (humidity_delta / 100)

        if wind_speed_mean > 15:
            prediction += WIND_SPEED_SHARE
        
        if wind_speed_mean > 3:
            prediction += WIND_DIRECTION_DELTA_SHARE * (1 - wind_direction_delta / 180)
            if wind_direction_change_delta > 0:
                prediction += WIND_DIRECTION_CHANGE_SHARE * (wind_direction_change_delta / 180)
        
        prediction += TEMPERATURE_ABS_SHARE * (1 - temperature_delta / 20)

        if temperature_change_delta > 0:
            prediction += TEMPERATURE_DELTA_SHARE * (temperature_change_delta / 20)


    new_prediction = RainPrediction(prediction=prediction, created_at=datetime.now())
    db.session.add(new_prediction)
    db.session.commit()


    automation_requests = AutomationRequest.query.filter(AutomationRequest.trigger == 'rain_prediction').all()
    for request in automation_requests:
        if automation_request_service.is_request_triggered(request, prediction):
            automation_request_service.send_http_request(request)
    
    if prediction > 1:
        return 1
    elif prediction < 0:
        return 0
    
    return prediction
