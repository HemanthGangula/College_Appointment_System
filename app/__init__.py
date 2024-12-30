from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.auth import auth_bp
from app.routes.availability import availability_bp
from app.routes.appointments import appointments_bp
from app.routes.mainpage import main_bp

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'hemanth226'

    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(availability_bp, url_prefix='/api')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    app.register_blueprint(main_bp) 

    return app