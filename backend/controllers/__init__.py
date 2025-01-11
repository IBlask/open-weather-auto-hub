from .measuring_device_controller import measuring_device_bp
from .weather_data_controller import weather_data_bp


def register_blueprints(app):
    app.register_blueprint(measuring_device_bp)
    app.register_blueprint(weather_data_bp)
