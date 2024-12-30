from .measuring_device_controller import measuring_device_bp


def register_blueprints(app):
    app.register_blueprint(measuring_device_bp)