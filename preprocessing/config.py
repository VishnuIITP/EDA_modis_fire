configs = {
    "csv": {
            "scale_cols": ["frp"],          # numeric column to scale
            "encode_cols": ["satellite"],   # categorical column to encode
            "target_col": "confidence",     # target variable
            "test_size": 0.2,               # 80/20 split
            "stratify": True,               # preserve class distribution
            "scaling": "minmax"             # choose 'minmax' or 'zscore'
    },
    "json": {
        "scale_cols": ["temperature", "humidity"],
        "encode_cols": ["region", "sensor_type"],
        "target_col": "alert_level",
        "test_size": 0.3,
        "stratify": True,
        "scaling": "zscore"
    }
}




def get_config(file_path, configs):
    if file_path.endswith(".csv"):
        return configs["csv"]
    elif file_path.endswith(".json"):
        return configs["json"]
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return configs["csv"]  # If Excel has the same schema, reuse CSV config
    else:
        raise ValueError("Unsupported format")
