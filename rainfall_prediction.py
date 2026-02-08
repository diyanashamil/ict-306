from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
import pandas as pd
import joblib
import os
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model(r'C:\Users\ZhangZiheng\Desktop\206\Project\rainfall_model.keras')

# Fit the scaler with dummy data containing 19 features
scaler = MinMaxScaler()
sample_data = [[0] * 19, [100] * 19]  # Replace 0 and 100 with actual min/max values for each feature if known
scaler.fit(sample_data)


@app.route('/')
def home():
    return render_template('index.html')
    
os.makedirs('data', exist_ok=True)
      
@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        print("Received data:", data)

        df = pd.DataFrame([data])
        print("DataFrame created:", df)

        csv_path = r'C:\Users\ZhangZiheng\Desktop\206\Project\data\weather_data.csv'
        df.to_csv(csv_path, mode='a', index=False, header=not os.path.exists(csv_path))
        print("Data saved successfully to", csv_path)

        return jsonify({"message": "Data saved successfully!"})

    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data for prediction:", data)

        # Extract all 19 features
        feature_values = [
            float(data.get('p', 0)), float(data.get('T', 0)), float(data.get('Tpot', 0)),
            float(data.get('Tdew', 0)), float(data.get('rh', 0)), float(data.get('VPmax', 0)),
            float(data.get('VPact', 0)), float(data.get('VPdef', 0)), float(data.get('sh', 0)),
            float(data.get('H2OC', 0)), float(data.get('rho', 0)), float(data.get('wv', 0)),
            float(data.get('max_wv', 0)), float(data.get('wd', 0)), float(data.get('SWDR', 0)),
            float(data.get('PAR', 0)), float(data.get('max_PAR', 0)), float(data.get('Tlog', 0)),
            float(data.get('rain', 0))
        ]
        print("Feature values:", feature_values)

        # Scale input data with 19 features
        scaled_input = scaler.transform([feature_values])[0]
        print("Scaled input data:", scaled_input)

        # Create sequence of 19 timesteps
        sequence_length = 19
        input_sequence = np.array([scaled_input] * sequence_length)
        input_sequence = input_sequence.reshape((1, sequence_length, len(feature_values)))
        print("Prepared input data for model:", input_sequence)

        # Predict rainfall
        prediction = model.predict(input_sequence)
        predicted_rainfall = float(prediction[0][0])  # Convert to standard float for JSON serialization
        print("Predicted rainfall:", predicted_rainfall)

        # Return result as JSON
        return jsonify({'rainfall_prediction': predicted_rainfall})

    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
