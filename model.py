import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\ZhangZiheng\Desktop\206\Project\data\weather_data.csv'
data = pd.read_csv(file_path)

# Use all columns except 'date' as features, and drop any rows with missing values
data = data.drop(columns=['date']).dropna()

# Initialize scalers for features and target (rain column)
feature_scaler = MinMaxScaler()
rain_scaler = MinMaxScaler()

# Scale the features (all columns except 'rain') and target ('rain') separately
scaled_features = feature_scaler.fit_transform(data.drop(columns=['rain']))
scaled_rain = rain_scaler.fit_transform(data[['rain']])

# Combine scaled features and target
scaled_data = np.hstack((scaled_features, scaled_rain))

# Function to create sequences for LSTM
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, :-1])  # Use all columns except the last one as features
        y.append(data[i, -1])  # Use the last column (rain) as target
    return np.array(X), np.array(y)

# Set sequence length to capture more historical data (e.g., last 120 timesteps)
sequence_length = 120
X, y = create_sequences(scaled_data, sequence_length)

# Split data into training and testing sets
training_size = int(len(X) * 0.8)
X_train, y_train = X[:training_size], y[:training_size]
X_test, y_test = X[training_size:], y[training_size:]

# Reshape for LSTM input (samples, timesteps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], X_train.shape[2]))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], X_test.shape[2]))

# Build a more complex LSTM model with additional layers and dropout layers
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.3))  # Drop 30% to reduce overfitting
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(25))
model.add(Dense(1))  # Output layer for regression

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model with increased epochs (200)
model.fit(X_train, y_train, epochs=200, batch_size=32)

# Save the model in Keras format
model.save(r'C:\Users\ZhangZiheng\Desktop\206\Project\rainfall_model.keras')

# Make predictions
predictions = model.predict(X_test)

# Inverse transform the predictions for the rain column only
predictions = rain_scaler.inverse_transform(predictions)

# Plot the results
actual_rainfall = rain_scaler.inverse_transform(y_test.reshape(-1, 1))  # Rescale y_test for comparison
plt.plot(actual_rainfall, color='blue', label='Actual Rainfall')
plt.plot(predictions, color='red', label='Predicted Rainfall')
plt.xlabel('Time')
plt.ylabel('Rainfall')
plt.legend()
plt.show()