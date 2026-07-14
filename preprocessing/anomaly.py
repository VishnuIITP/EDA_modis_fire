import pandas as pd


def detect_anomalies(df, column="confidence", low_threshold=54, high_threshold=95):
    """
    Detect anomalies based on a threshold in a given column.

    Args:
        df (pd.DataFrame): Input dataset
        threshold (float): Threshold value for anomaly detection
        column (str): Column to check anomalies on

    Returns:
        dict: anomaly count, anomaly percentage, anomaly dataframe
    """


        if column not in df.columns:
            return {"count": 0, "percentage": 0.0, "anomalies": pd.DataFrame()}

        anomalies = df[(df[column] < low_threshold) | (df[column] > high_threshold)]
        count = len(anomalies)
        percentage = (count / len(df)) * 100 if len(df) > 0 else 0

        return {"count": count, "percentage": percentage, "anomalies": anomalies}
