import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/shipments"

def test_full_lifecycle():
    # --- STEP 1: CREATE ---
    print("--- Step 1: Creating Shipment (POST) ---")
    payload = {
        "item_type": "Industrial Pump",
        "origin": "Hyderabad",
        "destination": "Bangalore",
        "created_by": "Logistics_Manager_01"
    }
    create_res = requests.post(BASE_URL, json=payload)
    if create_res.status_code != 201:
        print(f"❌ Creation failed: {create_res.text}")
        return
    
    tracking_id = create_res.json()['tracking_id']
    print(f"✅ Created! ID: {tracking_id}")

    # --- STEP 2: VERIFY INITIAL HISTORY ---
    print(f"\n--- Step 2: Checking Initial History (GET) ---")
    get_res = requests.get(f"{BASE_URL}/{tracking_id}")
    initial_data = get_res.json()
    print(f"Current Status: {initial_data['status']}")
    print(f"History Logs Found: {len(initial_data.get('history', []))}")

    # --- STEP 3: UPDATE (PUT) ---
    print(f"\n--- Step 3: Marking as Delivered (PUT) ---")
    update_payload = {"status": "Delivered"}
    put_res = requests.put(f"{BASE_URL}/{tracking_id}", json=update_payload)
    
    if put_res.status_code == 200:
        print(f"✅ Update successful: {put_res.json()['message']}")
    else:
        print(f"❌ Update failed: {put_res.text}")

    # --- STEP 4: FINAL AUDIT VERIFICATION ---
    print(f"\n--- Step 4: Final Audit Trail Verification (GET) ---")
    final_res = requests.get(f"{BASE_URL}/{tracking_id}")
    final_data = final_res.json()
    
    print(f"Final Status: {final_data['status']}")
    print(f"Final Received At: {final_data['received_at']}")
    
    print("\n--- Shipment Journey (Audit Trail) ---")
    history = final_data.get('history', [])
    for entry in history:
        print(f"📍 [{entry['timestamp']}] - Status: {entry['status']}")

    # Final Validation
    if len(history) >= 2 and final_data['received_at'] is not None:
        print("\n🎉 SUCCESS: The shipment was created, updated, and logged correctly!")
    else:
        print("\n❌ FAILURE: Audit trail or timestamp is missing.")

if __name__ == "__main__":
    test_full_lifecycle()