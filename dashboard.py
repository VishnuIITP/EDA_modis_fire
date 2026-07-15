import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page layout to wide (full screen)
st.set_page_config(layout="wide")

# Import pipeline modules
from preprocessing.loader import load_data
from preprocessing.preprocess import preprocess_data
from preprocessing.validate import validate_split
from preprocessing.config import configs, get_config
from api_client import call_prediction_api   # API client for Rupali's /predict endpoint

# Dashboard title
st.title("🔥 Preprocessing & Anomaly Detection Dashboard")

# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("Controls")

# Upload telemetry dataset
uploaded_file = st.sidebar.file_uploader("Upload Telemetry CSV/Excel/JSON", type=["csv", "json", "xlsx", "xls"])

# -------------------------------
# Main pipeline
# -------------------------------
if uploaded_file is not None:
    # 1. Load dataset
    df = load_data(uploaded_file)

    if df is not None:
        # 2. Get config based on file type
        config = get_config(uploaded_file.name, configs)

        # 3. Preprocess + Split
        X_train, X_test, y_train, y_test = preprocess_data(df, config)

        # 4. Validate split (developer mode, optional)
        validation_results = validate_split(X_train, X_test, y_train, y_test, config)

        # -------------------------------
        # Dataset Summary
        # -------------------------------
        st.header("📊 Dataset Summary")
        st.write(df.describe())

        # -------------------------------
        # Call Rupali's /predict API
        # -------------------------------
        prediction_results = call_prediction_api(df)  # send telemetry data to backend

        # -------------------------------
        # Prediction Summary Panel
        # -------------------------------
        col1, col2, col3 = st.columns(3)
        col1.metric("Records Processed", len(df))   # total records processed

        if prediction_results:
            if prediction_results["status"] == "error":
                # Show error in Streamlit instead of crashing
                st.error(f"API Error: {prediction_results['message']}")

            elif prediction_results["status"] == "waiting":
                # Case 1: Backend still collecting packets (<120)
                st.warning(
                     f"Packets received: {prediction_results['packets_received']} / "
                     f"{prediction_results['required_packets']}"
                )

            elif prediction_results["status"] == "success":
                # Case 2: Backend has enough packets and returns ML prediction
                ml_pred = prediction_results["ml_prediction"]

                # Convert API result into anomaly metrics
                anomalies = 1 if ml_pred["is_anomaly"] else 0
                anomaly_pct = (anomalies / len(df)) * 100

                col2.metric("Anomalies", anomalies)          # number of anomalies
                col3.metric("Anomaly %", f"{anomaly_pct:.2f}%")  # anomaly percentage

                # Show detailed prediction result
                st.subheader("Prediction Result")
                st.write("Model Name:", ml_pred["model_name"])
                st.write("Is Anomaly:", ml_pred["is_anomaly"])
                st.write("Label:", ml_pred["label"])
                st.write("Score:", ml_pred["score"])

                # Add anomaly flag to dataframe for visualization
                df["is_anomaly"] = ml_pred["is_anomaly"]

        # -------------------------------
        # Visualizations
        # -------------------------------
        st.header("📈 Visualizations")

        if config["target_col"] in df.columns:
            plt.figure(figsize=(8, 5))

            # Plot normal records (blue)
            if "is_anomaly" in df.columns and not df["is_anomaly"].all():
                sns.histplot(
                    df.loc[df["is_anomaly"] == False, config["target_col"]],
                    bins=30, color="skyblue", label="Normal Records"
                )

            # Plot anomalous records (red)
            if "is_anomaly" in df.columns and df["is_anomaly"].any():
                sns.histplot(
                    df.loc[df["is_anomaly"] == True, config["target_col"]],
                    bins=30, color="red", label="Anomalous Records"
                )

            plt.title(f"{config['target_col']} Distribution (Normal vs Anomalies)")
            plt.xlabel(config["target_col"])
            plt.ylabel("Frequency")
            plt.legend()
            st.pyplot(plt)

        # Optional time series visualization if datetime column exists
        if "datetime" in df.columns:
            st.line_chart(df.set_index("datetime")[config["target_col"]])

        # -------------------------------
        # Download Options
        # -------------------------------
        st.header("⬇️ Download Results")

        # Download processed dataset
        csv_processed = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Processed Dataset", csv_processed, "processed.csv", "text/csv")

        # Download prediction results (if available)
        if prediction_results and prediction_results["status"] == "success":
            csv_pred = pd.DataFrame([prediction_results["ml_prediction"]]).to_csv(index=False).encode("utf-8")
            st.download_button("Download Prediction Result", csv_pred, "prediction.csv", "text/csv")
