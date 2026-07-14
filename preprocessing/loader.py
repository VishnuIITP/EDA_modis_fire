import pandas as pd
import json

def load(file_path):
    """
    Loads a dataset from CSV, JSON, or Excel into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the dataset file

    Returns:
        DataFrame: Loaded dataset
    """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}. Please use CSV, JSON, or Excel.")

    print(f"Loaded dataset with shape {df.shape} from {file_path}")


    return df
