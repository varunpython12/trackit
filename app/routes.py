from flask import Blueprint, request,jsonify
from app.models import db, Shipment
from datetime import datetime

# A Blueprint organizes our routes into a modular 'package'
shipment_bp = Blueprint('shipment_bp', __name__)

@shipment_bp.route('/api/shipments', methods=['POST'])
def create_shipment():
    # 1. Get the data sent by the user (JSON format)
    data = request.get_json()

    # 2. Basic Validation: Ensure required fields exist
    if not data or 'item_type' not in data or 'origin' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    # 3. Create the Shipment Object (using the Class we built!)
    new_shipment = Shipment(
        item_type=data.get('item_type'),
        origin=data.get('origin'),
        destination=data.get('destination'),
        created_by=data.get('created_by','System_User') # Default if not provided
    )

    # 4. Save to Database
    try:
        db.session.add(new_shipment)
        db.session.commit()

        # 5. Return success message and the new ID
        return jsonify({
            "message": "Shipment creatd successfully",
            "tracking_id": new_shipment.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@shipment_bp.route('/api/shipments/<string:shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    # 1. Lookup the shipment in the database by its ID
    # This is like a 'SELECT * FROM shipments WHERE id = shipment_id'
    shipment = Shipment.query.get(shipment_id)

    # 2. If the shipment doesn't exist, return a 404 error
    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404
    
    # 3. If found, return the shipment details as JSON
    return jsonify({
        "tracking_id": shipment.id,
        "item_type": shipment.item_type,
        "origin": shipment.origin,
        "destination": shipment.destination,
        "status": shipment.current_status,
        "created_at": shipment.created_at.isoformat() if shipment.created_at else None,
        "received_at": shipment.received_at.isoformat() if shipment.received_at else None
    }), 200


@shipment_bp.route('/api/shipments/<string:shipment_id>', methods=['PUT'])
def update_status(shipment_id):
    # 1. Find the Shipment
    shipment = Shipment.query.get(shipment_id)
    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404
    
    # 2. Get the new status from the request
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "Status is required"}), 400
    
    # 3. Update the status
    shipment.current_status = new_status

    # 4. Special Logic: If delivered, set the timestamp
    if new_status.lower() == 'delivered':
        shipment.received_at = datetime.utcnow()
    
    # 5. Save to Database
    db.session.commit()

    return jsonify({
        "message": "Status updated successfully",
        "new_status": shipment.current_status,

        "received_at": shipment.received_at.isoformat() if shipment.received_at else None
    }), 200
