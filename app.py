from flask import Flask, render_template, request
import pandas as pd
import pickle

# Load the pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template('index.html')

# Details route
@app.route('/details')
def pred():
    return render_template('details.html')

# Predict route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            SIZE = request.form['SIZE']
            FUEL = request.form['FUEL']
            DISTANCE = request.form['DISTANCE']
            DESIBEL = request.form['DESIBEL']
            AIRFLOW = request.form['AIRFLOW']
            FREQUENCY = request.form['FREQUENCY']

            total = [[SIZE, FUEL, DISTANCE, DESIBEL, AIRFLOW, FREQUENCY]]
            d1 = pd.DataFrame(data=total, columns=['SIZE', 'FUEL', 'DISTANCE', 'DESIBEL', 'AIRFLOW', 'FREQUENCY'])

            # Make prediction using the model
            prediction = model.predict(d1)
            prediction = prediction[0]

            if prediction == 0:
                return render_template('results.html', prediction_text="The fire is in a non-extinction state.")
            else:
                return render_template('results.html', prediction_text="The fire is in an extinction state.")
        except KeyError as e:
            return f"Missing form field: {str(e)}", 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
