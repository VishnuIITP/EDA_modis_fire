

import streamlit as st
import requests
import time

# -------------------------------
# CONFIGURATION
# -------------------------------
API_HEALTH_URL = "http://localhost:8000/api/v1/health"
API_PREDICT_URL = "http://localhost:8000/api/v1/predict"

# -------------------------------
# FUNCTION: Check backend health
# -------------------------------
def check_backend_status():
    """
    Check if backend and model are available.
    Returns:
    - Backend status (Connected/Disconnected)
    - Model status (Available/Unavailable)
    """
    try:
        response = requests.get(API_HEALTH_URL, timeout=3)
        if response.status_code == 200:
            data = response.json()
            backend_status = "✅ Connected"
            model_status = "✅ Available" if data.get("model_status") == "available" else "❌ Unavailable"
        else:
            backend_status = "❌ Disconnected"
            model_status = "❌ Unknown"
    except Exception:
        backend_status = "❌ Disconnected"
        model_status = "❌ Unknown"
    return backend_status, model_status


# -------------------------------
# FUNCTION: Call prediction API
# -------------------------------
def call_prediction_api(payload):
    """Send sample telemetry data to backend and measure response time."""
    start_time = time.time()
    response = requests.post(API_PREDICT_URL, json=payload)
    elapsed = time.time() - start_time
    return response.json(), elapsed

# -------------------------------
# STREAMLIT DASHBOARD
# -------------------------------
st.set_page_config(page_title="Telemetry Dashboard", layout="wide")

st.title("🚀 Telemetry Dashboard")

# Sidebar: System Status Panel
st.sidebar.header("System Status")
backend_status, model_status = check_backend_status()
st.sidebar.write(f"Backend Status: {backend_status}")
st.sidebar.write(f"Model Status: {model_status}")

# Sidebar: How to Use Guide
st.sidebar.header("📘 How to Use")
st.sidebar.markdown("""
1. Dashboard checks backend health.  
2. Sample telemetry data is sent to API.  
3. View prediction result and response time.  
""")

# -------------------------------
# MAIN LAYOUT
# -------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Prediction Result")

    # Example telemetry payload (replace later with real dataset)
    sample_data = {
        "satellite_id": "SAT-001",
        "timestamp": "2026-07-17T10:00:00",
        "battery_voltage": 12.4,
        "temperature": 38.2,
        "cpu_usage": 43,
        "signal_strength": 91
    }

    result, response_time = call_prediction_api(sample_data)

    st.json(result)  # Show raw API response
    st.write(f"⏱ API Response Time: {response_time:.2f} seconds")

with col2:
    st.subheader("🗂 Dashboard Info")
    st.info("This panel shows backend connectivity, model availability, and prediction response time.")
