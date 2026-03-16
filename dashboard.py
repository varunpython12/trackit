import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuration
API_URL = "http://127.0.0.1:5000/api/shipments"

st.set_page_config(page_title="TrackIt Dashboard", page_icon="📦", layout="wide")

st.title("📦 TrackIt Logistics Management")
st.markdown("---")

# --- SIDEBAR: TRACKING ---
st.sidebar.header("🔍 Track Shipment")
search_id = st.sidebar.text_input("Enter Tracking ID")

if st.sidebar.button("Track"):
    if search_id:
        response = requests.get(f"{API_URL}/{search_id}")
        if response.status_code == 200:
            st.session_state['current_shipment'] = response.json()
        else:
            st.sidebar.error("Shipment not found. Check the ID.")
    else:
        st.sidebar.warning("Please enter an ID.")

# --- MAIN AREA: DISPLAY & UPDATES ---
if 'current_shipment' in st.session_state:
    data = st.session_state['current_shipment']
    
    # Header Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", data['status'])
    col2.metric("Origin", data['origin'])
    col3.metric("Destination", data['destination'])

    # Update Status Section
    st.subheader("Update Status")
    new_status = st.selectbox("Select New Status", ["In Transit", "Out for Delivery", "Delivered", "Delayed"])
    if st.button("Update Status"):
        res = requests.put(f"{API_URL}/{data['tracking_id']}", json={"status": new_status})
        if res.status_code == 200:
            st.success(f"Moved to {new_status}!")
            # Refresh data
            st.session_state['current_shipment'] = requests.get(f"{API_URL}/{data['tracking_id']}").json()
            st.rerun()

    # Audit Trail Table
    st.subheader("📜 Shipment Journey (Audit Trail)")
    df = pd.DataFrame(data['history'])
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%b %d, %Y - %H:%M')
    st.table(df)

else:
    st.info("Enter a Tracking ID in the sidebar to view details or create a new shipment below.")

# --- CREATE SECTION ---
st.markdown("---")
st.header("🆕 Register New Shipment")
with st.form("new_shipment"):
    item = st.text_input("Item Description (e.g., Industrial Pump)")
    origin = st.text_input("Origin")
    dest = st.text_input("Destination")
    submitted = st.form_submit_button("Create Shipment")

    if submitted:
        payload = {"item_type": item, "origin": origin, "destination": dest}
        res = requests.post(API_URL, json=payload)
        if res.status_code == 201:
            st.success(f"Created! ID: {res.json()['tracking_id']}")
        else:
            st.error("Error creating shipment.")