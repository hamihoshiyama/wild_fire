from flask import Flask, render_template, request
import joblib
import pandas as pd

#limit the months/ days they can put in 
# make it so they can still click to edit long and lat 
# prevent user from clicking to any other place except CA

app = Flask(__name__)

model = joblib.load('fire_class_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        month = int(request.form['month'])
        day = int(request.form['day'])

        input_data = pd.DataFrame({
            'latitude': [latitude],
            'longitude': [longitude],
            'month': [month],
            'day': [day]
        })

        prediction = int(model.predict(input_data)[0])  

        return render_template('index.html',
                               prediction_text=f"Predicted Fire Class: {prediction}",
                               fire_level=prediction)

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
