def validate_split(X_train, X_test, y_train, y_test, config):
    """
    Quick validation checks for preprocessed dataset.
    """
    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    # Target distribution check
    print("Target distribution in train:\n", y_train.value_counts(normalize=True))
    print("Target distribution in test:\n", y_test.value_counts(normalize=True))

    # Scaling check (only for numeric columns in config)
    for col in config["scale_cols"]:
        print(f"Scaled {col} range (train): {X_train[col].min()} to {X_train[col].max()}")

    # Missing values check
    print("Missing values in train:", X_train.isnull().sum().sum())
    print("Missing values in test:", X_test.isnull().sum().sum())

    # Encoding check
    for col in config["encode_cols"]:
        if col in X_train.columns:
            print(f"Unique values in {col} (train):", X_train[col].unique())
