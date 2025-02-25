from .measuring_device_controller import measuring_device_bp
from .weather_data_controller import weather_data_bp
from .automation_device_controller import automation_device_bp
from .email_controller import email_bp
from .automation_request_controller import automation_request_bp


def register_blueprints(app):
    app.register_blueprint(measuring_device_bp)
    app.register_blueprint(weather_data_bp)
    app.register_blueprint(automation_device_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(automation_request_bp)
