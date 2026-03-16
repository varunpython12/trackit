from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)

    # Configuration for our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackit.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with this app
    db.init_app(app)

    # Add these two lines to join the routes:
    from app.routes import shipment_bp
    app.register_blueprint(shipment_bp)

    return app