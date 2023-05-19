import math
from datetime import datetime, timedelta
import statistics as stat

from scipy.signal import find_peaks
from scipy.stats import pearsonr

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from joblib import load

import csv
import sqlite3

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DATABASE'] = 'database.db'

try:
    model = load('model.joblib') # load the trained model
except:
    print('No model found or model is not trained yet')

# ===================== DATABASE TABLE CREATE =====================
# Connect to the database
conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()

# Create a table TODO change the table so that it stores the data formated 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity TEXT NOT NULL,
        duration REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
# ===================== DATABASE TABLE CREATE END =====================

# ===================== FUNCTIONS =====================

#define the types of activities: hoja, tek, kolo.
types = {
    0: "hoja",
    1: "tek",
    2: "kolo"
}

def format_data(data): 
    # TODO format the data so that it can be used by the model
    # HOW WILL THE DATA LOOK LIKE WHEN IT IS SENT BY THE CLIENT?
    # Should we add some measures here like mean, std, peaks, etc.? could imporve prediction accuracy
    # if sending 10 samples at once they can be joined into more "accurate" data
    # Send same data when "training" and "predicting" the activity

    return 0 

#helper function to test the database connection
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn
# ===================== FUNCTIONS END =====================


# ===================== APP ROUTES =====================
# define the root of the server
@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, World!'

# ===================== COLECTING DATA =====================
# section for collecting data to train the model
# define the endpoints for saving the data during the training process

app.config['DATA'] = []     # global variable to store the data temporarily

# this endpoint should be called when tracking is active(TRACK button) the data and the label are sent by ESP board every ?? seconds 
# (hoja: 0 , tek: 1 , kolo: 2)?
@app.route('/data', methods=['POST'])
@cross_origin()
def save_data():

    # get the data from the request
    data = request.get_json() #maybe only gate data and the label here?

    formated = format_data(data) #format the data so that it can be used by the model

    # add the data to the global variable
    app.config['DATA'].append(formated)

    return 'Data saved successfully', 200

# this endpoint should be called when the training process is finished (STOP button)
# the data that has been sent do far will be saved to a single csv file 
@app.route('/save-csv', methods=['PUT'])
@cross_origin()
def save_to_csv():
    data = app.config['DATA']
    if len(data) == 0:
        return 'No data available', 404

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H-%M-%S')
    label = 'example_label'  # TODO get labelfrom data sent by the client and put it here

    file_name = f'data_{current_date}_{current_time}_{label}.csv'
    
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() # TODO check if here is the correct format?? 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return f'Data saved to {file_name}', 200

# ======================== PREDICTING ACTIVITY ========================
# section for predicting the activity and saving the data to a database 

# this endpoint predicts the activity and saves it to the database
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict_save():
    global model 
    
    #get data and format it
    data = request.get_json() # get data from request body
    features = format_data(data) # this functions does not work yet

    # Perform prediction using the model TODO cast to type of activity?? what does the model return?
    activity = model.predict([features])[0]
    duration = 0.25 # TODO calculate the duration of the activity or set as static value?
    
    # Connect to the database
    conn = get_db()
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO readings (activity, duration)
        VALUES (?, ?)
    ''', (activity, duration))
    # Timestapm is added automatically (curent time)
    
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

    return jsonify({'activity': activity}), 200

# ======================== GETTING DATA FROM DATAABSE ========================
# TODO add an endpoint that will return the data from the database in a JSON format
# TODO endpoint for current activity (last row in the database)?  

# testing the database connection endpoint
@app.route('/test-database')
@cross_origin()
def test_database():
    try:
        conn = get_db()
        conn.execute('SELECT 1')
        return 'Database connection successful'
    except Exception as e:
        return f'Database connection failed: {str(e)}'


# endpoint for getting the last entry from the database if it has been added in the last 10 secondss
@app.route('/latest-entry')
@cross_origin()
def get_latest_entry():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Calculate the timestamp threshold
        threshold = datetime.now() - timedelta(seconds=10)

        # Query the latest entry within the last 10 seconds
        cursor.execute('''
            SELECT *
            FROM readings
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (threshold,))

        entry = cursor.fetchone()

        if entry:
            # Convert the timestamp to a string format
            timestamp_str = entry[2].strftime('%Y-%m-%d %H:%M:%S')
            # Create a response JSON object
            response = {
                'activity': entry[0],
                'duration': entry[1],
                'timestamp': timestamp_str
            }
            return jsonify(response), 200
        else:
            return 'No recent entries found', 404

    except Exception as e:
        return f'Error retrieving latest entry: {str(e)}', 500

# endpoint for getting the data from the database for the current week
@app.route('/weekly-data')
@cross_origin()
def get_weekly_data():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get the start and end dates for the current week
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Query the data for the current week
        cursor.execute('''
            SELECT activity, date(timestamp), SUM(duration)
            FROM readings
            WHERE date(timestamp) BETWEEN ? AND ?
            GROUP BY activity, date(timestamp)
        ''', (start_of_week, end_of_week))

        activity_data = cursor.fetchall()

        # Calculate distance and calories using the duration and factors
        factor_distance = 1  # Change this value as needed
        factor_calories = 1  # Change this value as needed

        data = []

        # Iterate over the activity data and calculate distance and calories
        for entry in activity_data:
            activity = entry[0]
            date = entry[1]
            duration = entry[2]

            # TODO different factors for different activities (walking, running, cycling)   
            distance = duration * factor_distance
            calories = duration * factor_calories

            # Create a dictionary with the activity, date, duration, distance, and calories
            data.append({
                'activity': activity,
                'date': date,
                'duration': duration,
                'distance': distance,
                'calories': calories
            })

        return jsonify(data), 200

    except Exception as e:
        return f'Error retrieving weekly data: {str(e)}', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)