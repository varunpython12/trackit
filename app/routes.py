from flask import Blueprint, request,jsonify
from app.models import db, Shipment

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