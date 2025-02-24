from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

try:
    model = joblib.load('fire_class_model.pkl')
    app.logger.info("Model loaded successfully.")
except Exception as e:
    app.logger.error(f"Failed to load model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fireinfo')
def fireinfo():
    # This is the page that shows the fire prediction details
    return render_template('fireinfo.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive and log incoming data
        data = request.get_json()
        app.logger.info(f"📥 Received data: {data}")

        # Parse input data
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        month = int(data['month'])
        day = int(data['day'])

        # Prepare input data for the model
        input_data = pd.DataFrame({
            'latitude': [latitude],
            'longitude': [longitude],
            'month': [month],
            'day': [day]
        })

        app.logger.info(f"🛠️ Prepared input data: {input_data}")

        # Make prediction
        prediction = int(model.predict(input_data)[0])
        app.logger.info(f"🔥 Prediction result: {prediction}")

        # Return prediction
        return jsonify({
            'prediction_text': f"Predicted Fire Class: {prediction}",
            'fire_level': prediction
        })

    except Exception as e:
        app.logger.error(f"❗ Error during prediction: {e}")
        return jsonify({'prediction_text': f"Error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/fireinfo')

def fireinfo():
  return render_template('fireinfo.html')
