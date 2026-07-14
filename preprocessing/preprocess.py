# Define Preprocessing Pipeline Function

from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

def preprocess_data(df, config):
    """
    Preprocesses the dataset based on configuration.

    Parameters:
        df (DataFrame): Input dataset
        config (dict): Configuration dictionary with keys:
            - scale_cols: list of numeric columns to scale
            - encode_cols: list of categorical columns to encode
            - target_col: target column name
            - test_size: fraction for test split (default 0.2)
            - stratify: whether to stratify split (default True)
            - scaling: 'zscore' or 'minmax'

    Returns:
        X_train, X_test, y_train, y_test
    """

    # Copy dataset
    data = df.copy()

    # Missing value handling
    data = data.dropna()   # or data.fillna(0) depending on strategy


    # Scaling
    if config.get("scaling") == "zscore":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()

    data[config["scale_cols"]] = scaler.fit_transform(data[config["scale_cols"]])

    # Encoding categorical columns
    for col in config["encode_cols"]:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])

    # Split features and target
    X = data.drop(columns=[config["target_col"]])
    y = data[config["target_col"]]

    # Train/test split
    stratify = y if config.get("stratify", True) else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.get("test_size", 0.2), stratify=stratify, random_state=42
    )

    print(f"Preprocessed dataset: {data.shape} rows, {data.shape[1]} columns")

    return X_train, X_test, y_train, y_test
