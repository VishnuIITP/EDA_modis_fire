import requests


API_URL = "https://psychic-disco-x54x7vqqjvq6fpgv4-8000.app.github.dev/api/v1/predict"

def call_prediction_api(df):
    """
    Sends telemetry data to Rupali's /predict API endpoint
    and returns the prediction results.
    """
    try:
        # Convert dataframe to JSON payload
        payload = df.to_dict(orient="records")

        # Send POST request to backend
        response = requests.post(API_URL, json=payload, timeout=10)

        # If successful, return JSON response
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"API call failed with status {response.status_code}"
            }

    except requests.exceptions.RequestException as e:
        # Catch ALL request-related errors (connection, timeout, DNS, etc.)
        return {
            "status": "error",
            "message": str(e)
        }





