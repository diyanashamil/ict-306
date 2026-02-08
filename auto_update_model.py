import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# Paths
data_path = r'C:\Users\ZhangZiheng\Desktop\206\Project\data\weather_data.csv'
model_path = r'C:\Users\ZhangZiheng\Desktop\206\Project\rainfall_model.keras'

# Parameters
BATCH_SIZE = 32

# Load scaler (assuming you've already fit a scaler and saved it if needed)
scaler = MinMaxScaler()

def load_and_preprocess_data():
    # Load data from CSV
    data = pd.read_csv(data_path)

    # Scale data and reshape as needed for training
    scaled_data = scaler.fit_transform(data)
    X, y = prepare_training_data(scaled_data)
    return X, y

def prepare_training_data(data):
    # Convert your data into appropriate shape for LSTM
    # This function should be adapted from your existing code in model.py
    # Example:
    X, y = [], []
    for i in range(len(data) - 19):  # Assuming 19 timesteps for the model
        X.append(data[i:i+19, :-1])  # Features
        y.append(data[i+19, -1])     # Target (e.g., rainfall)
    return np.array(X), np.array(y)

def update_model():
    # Load the model
    model = load_model(model_path)

    # Load new data
    X, y = load_and_preprocess_data()

    # Train the model on the new data
    model.fit(X, y, epochs=1, batch_size=BATCH_SIZE, verbose=1)

    # Save the updated model
    model.save(model_path)
    print("Model updated and saved.")

def monitor_data():
    # Track the last known number of entries
    last_count = 0

    while True:
        # Get current number of rows in data file
        current_count = sum(1 for row in open(data_path)) - 1  # Exclude header
        if current_count >= last_count + 5:
            print("5 new entries detected. Updating model...")
            update_model()
            last_count = current_count
        else:
            print("Waiting for more data...")

# Run the monitor
if __name__ == "__main__":
    monitor_data()
