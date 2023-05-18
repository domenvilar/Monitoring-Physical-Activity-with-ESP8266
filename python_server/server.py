import math
from datetime import datetime
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
        duration INTEGER,
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


# TODO this only saves the data to the database need to make an endpoint that will predict the data first
# and then save it to the database
# @app.route('/save-reading', methods=['POST'])
# @cross_origin()
# def save_reading():
#     data = request.get_json()

#     activity = data.get('activity')
#     duration = data.get('duration')

#     if not activity:
#         return 'Activity field is required', 400

#     # Connect to the database
#     conn = sqlite3.connect(app.config['DATABASE'])
#     cursor = conn.cursor()

#     # Insert data into the table
#     cursor.execute('''
#         INSERT INTO readings (activity, duration)
#         VALUES (?, ?)
#     ''', (activity, duration))

#     # Commit the changes
#     conn.commit()

#     # Close the connection
#     conn.close()

#     return 'Reading saved successfully', 200


# this endpoint predicts the activity and saves it to the database
@app.route('/predict', methods=['POST'])
@cross_origin()
def predict_save():
    global model 
    
    #get data and format it
    data = request.get_json() # get data from request body
    features = format_data(data) # this functions does not work yet

    # Perform prediction using the model TODO cast to type of activity?? 
    activity = model.predict([features])[0]
    duration = 0 # TODO calculate the duration of the activity or set as static value?
    
    # Connect to the database
    conn = sqlite3.connect(app.config['DATABASE'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)