# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from preprocessing.loader import load
from preprocessing.config import get_config, configs
from preprocessing.preprocess import preprocess_data
from preprocessing.validate import validate_split

file_path = "modis_2024_India.csv"
df = load(file_path)
config = get_config(file_path, configs)
X_train, X_test, y_train, y_test = preprocess_data(df, config)
validate_split(X_train, X_test, y_train, y_test, config)

