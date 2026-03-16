from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Shipment(db.Model):
    __tablename__ = "shipments"

    # Using String(36) to store the UUID as a string
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_type = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    current_status = db.Column(db.String(50), default='Pending')
    created_by = db.Column(db.String(100), nullable=False)
    received_by = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    received_at = db.Column(db.DateTime, nullable=True)


    # This links to the StatusLog table
    history = db.relationship('StatusLog', backref='shipment', lazy=True)

class StatusLog(db.Model):
    __tablename__ = "status_logs"

    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.String(36), db.ForeignKey('shipments.id'), nullable=False)
    status_reached = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)