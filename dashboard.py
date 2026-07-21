# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Set page layout to wide (full screen)
# st.set_page_config(layout="wide")
#
# # Import pipeline modules
# from preprocessing.loader import load_data
# from preprocessing.preprocess import preprocess_data
# from preprocessing.validate import validate_split
# from preprocessing.config import configs, get_config
# from api_client import call_prediction_api   # API client for Rupali's /predict endpoint
#
# # Dashboard title
# st.title("🔥 Preprocessing & Anomaly Detection Dashboard")
#
# # -------------------------------
# # Sidebar controls
# # -------------------------------
# st.sidebar.header("Controls")
#
# # Upload telemetry dataset
# uploaded_file = st.sidebar.file_uploader("Upload Telemetry CSV/Excel/JSON", type=["csv", "json", "xlsx", "xls"])
#
# # -------------------------------
# # Main pipeline
# # -------------------------------
# if uploaded_file is not None:
#     # 1. Load dataset
#     df = load_data(uploaded_file)
#
#     if df is not None:
#         # 2. Get config based on file type
#         config = get_config(uploaded_file.name, configs)
#
#         # 3. Preprocess + Split
#         X_train, X_test, y_train, y_test = preprocess_data(df, config)
#
#         # 4. Validate split (developer mode, optional)
#         validation_results = validate_split(X_train, X_test, y_train, y_test, config)
#
#         # -------------------------------
#         # Dataset Summary
#         # -------------------------------
#         st.header("📊 Dataset Summary")
#         st.write(df.describe())
#
#         # -------------------------------
#         # Call Rupali's /predict API
#         # -------------------------------
#         prediction_results = call_prediction_api(df)  # send telemetry data to backend
#
#         # -------------------------------
#         # Prediction Summary Panel
#         # -------------------------------
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Records Processed", len(df))   # total records processed
#
#         if prediction_results:
#             if prediction_results["status"] == "error":
#                 # Show error in Streamlit instead of crashing
#                 st.error(f"API Error: {prediction_results['message']}")
#
#             elif prediction_results["status"] == "waiting":
#                 # Case 1: Backend still collecting packets (<120)
#                 st.warning(
#                      f"Packets received: {prediction_results['packets_received']} / "
#                      f"{prediction_results['required_packets']}"
#                 )
#
#             elif prediction_results["status"] == "success":
#                 # Case 2: Backend has enough packets and returns ML prediction
#                 ml_pred = prediction_results["ml_prediction"]
#
#                 # Convert API result into anomaly metrics
#                 anomalies = 1 if ml_pred["is_anomaly"] else 0
#                 anomaly_pct = (anomalies / len(df)) * 100
#
#                 col2.metric("Anomalies", anomalies)          # number of anomalies
#                 col3.metric("Anomaly %", f"{anomaly_pct:.2f}%")  # anomaly percentage
#
#                 # Show detailed prediction result
#                 st.subheader("Prediction Result")
#                 st.write("Model Name:", ml_pred["model_name"])
#                 st.write("Is Anomaly:", ml_pred["is_anomaly"])
#                 st.write("Label:", ml_pred["label"])
#                 st.write("Score:", ml_pred["score"])
#
#                 # Add anomaly flag to dataframe for visualization
#                 df["is_anomaly"] = ml_pred["is_anomaly"]
#
#         # -------------------------------
#         # Visualizations
#         # -------------------------------
#         st.header("📈 Visualizations")
#
#         if config["target_col"] in df.columns:
#             plt.figure(figsize=(8, 5))
#
#             # Plot normal records (blue)
#             if "is_anomaly" in df.columns and not df["is_anomaly"].all():
#                 sns.histplot(
#                     df.loc[df["is_anomaly"] == False, config["target_col"]],
#                     bins=30, color="skyblue", label="Normal Records"
#                 )
#
#             # Plot anomalous records (red)
#             if "is_anomaly" in df.columns and df["is_anomaly"].any():
#                 sns.histplot(
#                     df.loc[df["is_anomaly"] == True, config["target_col"]],
#                     bins=30, color="red", label="Anomalous Records"
#                 )
#
#             plt.title(f"{config['target_col']} Distribution (Normal vs Anomalies)")
#             plt.xlabel(config["target_col"])
#             plt.ylabel("Frequency")
#             plt.legend()
#             st.pyplot(plt)
#
#         # Optional time series visualization if datetime column exists
#         if "datetime" in df.columns:
#             st.line_chart(df.set_index("datetime")[config["target_col"]])
#
#         # -------------------------------
#         # Download Options
#         # -------------------------------
#         st.header("⬇️ Download Results")
#
#         # Download processed dataset
#         csv_processed = df.to_csv(index=False).encode("utf-8")
#         st.download_button("Download Processed Dataset", csv_processed, "processed.csv", "text/csv")
#
#         # Download prediction results (if available)
#         if prediction_results and prediction_results["status"] == "success":
#             csv_pred = pd.DataFrame([prediction_results["ml_prediction"]]).to_csv(index=False).encode("utf-8")
#             st.download_button("Download Prediction Result", csv_pred, "prediction.csv", "text/csv")

#    st.info("This panel shows backend connectivity, model availability, and prediction response time.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import time

# -------------------------------
# CONFIGURATION
# -------------------------------
# “We use two API endpoints: /health to check backend and model availability, and
# /predict to send datasets for anomaly detection.
# This separation improves stability — the dashboard won’t attempt predictions if the backend isn’t ready.”
API_HEALTH_URL = "http://localhost:8000/api/v1/health"
API_PREDICT_URL = "http://localhost:8000/api/v1/predict"

# Import pipeline modules
from preprocessing.loader import load_data
from preprocessing.preprocess import preprocess_data
from preprocessing.validate import validate_split, validate_dataset, validate_class_distribution
from preprocessing.config import configs

# -------------------------------
# FUNCTION: Check backend health
# -------------------------------
def check_backend_status():
    """Check if backend and model are available."""
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
    """Send dataset to backend prediction API and measure response time."""
    start_time = time.time()
    response = requests.post(API_PREDICT_URL, json=payload)
    elapsed = time.time() - start_time
    return response.json(), elapsed

# -------------------------------
# STREAMLIT DASHBOARD
# -------------------------------
st.set_page_config(page_title="🔥 Preprocessing & Telemetry Dashboard", layout="wide")
st.title("🔥 Preprocessing & Anomaly Detection Dashboard")

# Sidebar: System Status Panel
st.sidebar.header("System Status")
backend_status, model_status = check_backend_status()
st.sidebar.write(f"Backend Status: {backend_status}")
st.sidebar.write(f"Model Status: {model_status}")

# Sidebar: Upload dataset
st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV/JSON)", type=["csv", "json"])

# -------------------------------
# MAIN PIPELINE
# -------------------------------
if uploaded_file is not None:
    # 1. Load dataset + detect type
    df, dataset_type = load_data(uploaded_file)

    # 2. Validate dataset
    valid, message = validate_dataset(df, dataset_type)
    st.info(message)
    if not valid:
        st.stop()

    # -------------------------------
    # Dataset Summary
    # -------------------------------
    st.header("📊 Dataset Summary")
    st.write(df.describe())

    #  Preprocess DataFrame before sending to API
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
    df["battery_voltage"] = df["battery_voltage"].clip(lower=0)
    df["cpu_usage"] = df["cpu_usage"].clip(lower=0, upper=100)

    #  Call prediction API
    with st.spinner("Running predictions..."):
        payload = df.to_dict(orient="records")
        prediction_results, response_time = call_prediction_api(payload)
        st.write("DEBUG Response Sample:", prediction_results[0])

    st.success("✅ Predictions complete")
    st.write(f"⏱ API Response Time: {response_time:.2f} seconds")

    # Summary metrics
    anomalies = sum(1 for res in prediction_results if res["ml_prediction"]["is_anomaly"])
    total = len(prediction_results)

    st.metric("Total Records", total)
    st.metric("Anomalies Detected", anomalies)


    # -------------------------------
    plt.figure(figsize=(8, 5))
    sns.histplot(df[configs[dataset_type]["target_col"]], bins=30, color="skyblue")
    plt.title(f"{configs[dataset_type]['target_col']} Distribution")
    plt.xlabel(f"{configs[dataset_type]['target_col']} Value")
    plt.ylabel("Record Count")
    st.pyplot(plt)


    # -------------------------------
    # Download Options
    # -------------------------------
    st.header("⬇️ Download Results")
    csv_processed = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Cleaned Dataset", csv_processed, "processed.csv", "text/csv")

