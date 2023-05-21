from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from joblib import load
import logging
import csv
import sqlite3
import pandas as pd
import math

app = Flask(__name__) # define app using Flask
cors = CORS(app, resources={r"*": {"origins": "*"}}) # enable CORS
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DATABASE'] = 'database.db' # define database file

# load the trained model
try:
    model = load('model.joblib')
except:
    print('No model found or model is not trained yet')


# ===================== DATABASE TABLE CREATE =====================
# Connect to the database
conn = sqlite3.connect(app.config['DATABASE'])
cursor = conn.cursor()

# Create the table if it doesn't exist
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

# ===================== HELPER FUNCTIONS =====================

def calculate_average(data, data_type):
    
    #check which data type is it
    if data_type == 'acc':
        data_key_prefix = 'acc'
    elif data_type == 'gyro':
        data_key_prefix = 'gyro'
    else:
        raise ValueError('Invalid data type. Must be either "acc" or "gyro".')

    acc_x_values = []
    acc_y_values = []
    acc_z_values = []

    # Extract the acceleration or gyro values from the data
    data_entries = data[data_type]

    # Loop through the data entries and extract the values
    for entry in data_entries:
        acc_x_values.append(entry['x'])
        acc_y_values.append(entry['y'])
        acc_z_values.append(entry['z'])

    # Calculate the average values
    avg_acc_x = sum(acc_x_values) / len(acc_x_values)
    avg_acc_y = sum(acc_y_values) / len(acc_y_values)
    avg_acc_z = sum(acc_z_values) / len(acc_z_values)

    # Return the average values as a dictionary whit type of data as key
    average_data = {
        f'avg_{data_key_prefix}_x': avg_acc_x,
        f'avg_{data_key_prefix}_y': avg_acc_y,
        f'avg_{data_key_prefix}_z': avg_acc_z
    }

    return average_data

# rename the keys in the dictionary add 1-10 to the end of each key name
# and join 10 rows into 1 row for better model training
def merge_10rows(data):

    # pop the label from the dictionary
    for dict in data:
        label = dict.pop('label')

    # make sure the data length is divisible by 10 
    # (so that we can merge 10 dictionaries into 1)
    data = data[:len(data) - (len(data) % 10)]

    # rename the keys in the dictionary add 1-10 to the end of each key name
    renamed_data = []
    index = 0
    for item in data:
        renamed_item = {}
        if index > 9:
            index = 0
        for key, value in item.items():
            new_key = f'{key}_{index}'  # Add the index to the key name
            renamed_item[new_key] = value
        index += 1
        renamed_data.append(renamed_item)

    #merge the data into batches of 10 (keys that have 1-10 go in the same batch)
    merged_data = []
    batch_size = 10
    for i in range(0, len(renamed_data), batch_size):
        batch = renamed_data[i:i+batch_size]
        merged_dict = {}
        for item in batch:
            merged_dict.update(item)
        merged_data.append(merged_dict)

    return merged_data

#merge the acc and gyro data into one dictionary 1 row is 10 rows of acc and 10 rows gyro data
def merge_acc_gyro(acc_data, gyro_data):

    # remeber the lable of the data
    label = acc_data[0]['label']

    merged_data_acc = merge_10rows(acc_data)
    merged_data_gyro = merge_10rows(gyro_data)

    data_combined = []

    for entry in zip(merged_data_acc, merged_data_gyro):
        data_combined.append(dict(entry[0], **entry[1]))

    # add the label back to the dictionary
    for dictio in data_combined:
        dictio['label'] = label
    
    return data_combined

# rename the keys in the dictionary add 1-10 to the end of each key name
# and join 10 rows into 1 row for better model predictions
def merge_10rows_tracking(data):


    # make sure the data length is divisible by 10 
    # (so that we can merge 10 dictionaries into 1)
    data = data[:len(data) - (len(data) % 10)]

    # rename the keys in the dictionary add 1-10 to the end of each key name
    renamed_data = []
    index = 0
    for item in data:
        renamed_item = {}
        if index > 9:
            index = 0
        for key, value in item.items():
            new_key = f'{key}_{index}'  # Add the index to the key name
            renamed_item[new_key] = value
        index += 1
        renamed_data.append(renamed_item)

    #merge the data into batches of 10 (keys that have 1-10 go in the same batch)
    merged_data = []
    batch_size = 10
    for i in range(0, len(renamed_data), batch_size):
        batch = renamed_data[i:i+batch_size]
        merged_dict = {}
        for item in batch:
            merged_dict.update(item)
        merged_data.append(merged_dict)

    return merged_data

#merge the acc and gyro data into one dictionary 1 row is 10 rows of acc and gyro data
def merge_acc_gyro_track(acc_data, gyro_data):

    #get rid of duration
    for diction in acc_data:
        diction.pop('duration')
    for diction in gyro_data:
        diction.pop('duration')


    merged_data_acc = merge_10rows_tracking(acc_data)
    merged_data_gyro = merge_10rows_tracking(gyro_data)

    data_combined = []

    for entry in zip(merged_data_acc, merged_data_gyro):
        data_combined.append(dict(entry[0], **entry[1]))

    return data_combined

#helper function to test the database connection
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


# ===================== APP ROUTES =====================
# define the root of the server
@app.route('/')
@cross_origin()
def hello_world():
    # return the temporary array of training data 
    return jsonify("DEBUG: Server reachable", app.config['DATA_ACC'], app.config['DATA_GYRO']), 200


# ===================== COLECTING DATA =====================
# section for collecting data to train the model
app.config['DATA_ACC'] = []     # global variable to store the data temporarily
app.config['DATA_GYRO'] = []     # global variable to store the data temporarily

# this endpoint should be called when collection is active the data and the label are sent by ESP board and stored in the global variable
@app.route('/data', methods=['POST'])
@cross_origin()
def save_collection_data():

    # get the data from the request
    data = request.get_json() 
    keys = list(data) #should be acc or gyro 


    #check if the data is valid
    if keys[0] == 'acc': 
        cache = 'DATA_ACC'
    elif keys[0] == 'gyro': 
        cache = 'DATA_GYRO'
    else:
        # errror 
        print(f"Data type error, key {keys} not supoorted")
        return jsonify('Data type error'), 500
    
    #format the data (avg 10 samples)
    formated = calculate_average(data, keys[0])

    #add label to the data
    formated['label'] = data[keys[0]][0]['label']

    #duration data is not needed for the model

    #add data to global variable
    app.config[cache].append(formated)


    return jsonify('Data bufferd successfully'), 200

# this endpoint should be called when the collecting process is finished (STOP button)
# the data that has been sent so far will be saved to a single csv file
@app.route('/save-csv', methods=['PUT'])
@cross_origin()
def save_to_csv():
    data_acc = app.config['DATA_ACC']
    data_gyro = app.config['DATA_GYRO']
    
    #check that there is some data avaliable to save
    if len(data_acc) < 10 or len(data_gyro) < 10:
        print("ERROR: No data for gyro or acc available:")
        print(f'[DEBUG] Length of data_acc: {len(data_acc)}')
        print(f'[DEBUG] Length of data_gyro: {len(data_gyro)}')

        return jsonify('No data for gyro or acc available'), 404
    
    # empty the global variables
    app.config['DATA_ACC'] = []
    app.config['DATA_GYRO'] = []

    #get the label from the data
    label = data_acc[0]['label']


    #make sure that the data is the same length
    if len(data_acc) != len(data_gyro):
        #make the longer list the same length as the shorter one
        if len(data_acc) > len(data_gyro):
            data_acc = data_acc[:len(data_gyro)]
        else:
            data_gyro = data_gyro[:len(data_acc)]

    #combine the data from acc and gyro
    data = merge_acc_gyro(data_acc, data_gyro)
    
    #save the data to a csv file include date, time and lable in the file name
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H-%M-%S')
    file_name = f'training_data/data_{current_date}_{current_time}_{label}.csv'
    
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return jsonify(f'Data saved to {file_name}'), 200

# ======================== PREDICTING ACTIVITY ========================
# section for predicting the activity and saving the data to a database 

app.config['DATA_ACC_TRACK'] = []   # global variable to store the data temporarily
app.config['DATA_GYRO_TRACK'] = []  # global variable to store the data temporarily
last_activity = "Unknown"           # global variable to store the last activity

#endpoint to disply the data that is being tracked and temporarly stored
@app.route('/track-data')
@cross_origin()
def track_data_show():
    # return the temporary array of data 
    return jsonify("DEBUG: Server reachable", app.config['DATA_ACC_TRACK'], app.config['DATA_GYRO_TRACK']), 200

# send data here when tracking is active to be stored in the global variable
@app.route('/tracking', methods=['POST'])
@cross_origin()
def save_tracking_data():

    # get the data from the request
    data = request.get_json() 
    keys = list(data) #should be acc or gyro

    #check if the data is valid
    if keys[0] == 'acc': 
        cache = 'DATA_ACC_TRACK'
    elif keys[0] == 'gyro': 
        cache = 'DATA_GYRO_TRACK'
    else:
        # errror 
        print(f"Data type error, key {keys} not supoorted")
        return jsonify('Data type error'), 500
    
    #avrage the 10 samples you recived from ESP board
    formated = calculate_average(data, keys[0]) 

    #add duration to the data
    formated['duration'] = data[keys[0]][0]['duration'] 
    
    #add data to global variable
    app.config[cache].append(formated)


    return jsonify('Data saved successfully'), 200


# this endpoint predicts the activity and saves it to the database
@app.route('/predict', methods=['GET'])
@cross_origin()
def predict_save():
    global model 
    global last_activity

    #check if there is enough data to predict the activity
    if len(app.config['DATA_ACC_TRACK']) < 10 or len(app.config['DATA_GYRO_TRACK']) < 10:
        #if not return unknown/latest activity
        print(f"[DEBUG] Not enough data... returning last activity: {last_activity}")
        
        return jsonify({'activity_type': last_activity}), 200 
    
    #if there is enough data to predict the activity combine it and predict the activity
    
    #take only the first 10 samples from the data
    data_acc = app.config['DATA_ACC_TRACK'][:10]
    data_gyro = app.config['DATA_GYRO_TRACK'][:10]

    #delete the data from the global variable
    app.config['DATA_ACC_TRACK'] = app.config['DATA_ACC_TRACK'][10:]
    app.config['DATA_GYRO_TRACK'] = app.config['DATA_GYRO_TRACK'][10:]

    duration_one = data_acc[0]['duration'] #get the duration of one sample of the activity

    #combine the data from acc and gyro
    data = merge_acc_gyro_track(data_acc, data_gyro)
    
    # convert the data to a dataframe
    data = pd.DataFrame(data)

    #predict the activity
    prediction = model.predict(data)

    last_activity = prediction[0]

    #calculate the duration of the activity 10 samples are combined to one prediction
    duration = duration_one * 10

    #save the prediction to the database
    # Connect to the database
    conn = get_db()
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO readings (activity, duration)
        VALUES (?, ?)
    ''', (prediction[0], duration))
    # Timestapm is added automatically (curent time)
    
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

    return jsonify({'activity_type': prediction[0]}), 200

# ======================== GETTING DATA FROM DATABASE ========================

# testing the database connection endpoint
@app.route('/test-database')
@cross_origin()
def test_database():
    try:
        conn = get_db()
        conn.execute('SELECT 1')
        return jsonify('Database connection successful'), 200
    except Exception as e:
        return jsonify(f'Database connection failed: {str(e)}'), 500

# endpoint for getting all the data from the database (to debug)
@app.route('/get-data')
@cross_origin()
def get_data():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Query all the data from the table
        cursor.execute('''
            SELECT *
            FROM readings
        ''')

        # Fetch all the data
        data = cursor.fetchall()

        print(f"[DEBUG] data from database: {data}")
        return jsonify(data), 200
    except Exception as e:
        return jsonify(f'Failed to get data from the database: {str(e)}'), 500
 
# endpoint for getting the last entry from the database if it has been added in the last 10 seconds (not needed for implementation)
@app.route('/latest-entry')
@cross_origin()
def get_latest_entry():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Calculate the timestamp threshold
        threshold = datetime.now() - timedelta(seconds=12)

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
            # Create a response JSON object
            response = {
                'activity': entry[0],
                'duration': entry[1],
                'timestamp':entry[2]
            }
            
            return jsonify(response), 200
        else:
            return 'No recent entries found', 404

    except Exception as e:
        return jsonify(f'Error retrieving latest entry: {str(e)}'), 500


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

        # Fetch all the data
        activity_data = cursor.fetchall() # [(activity, date, duration), ...]

        # aggregate data for each day (mon, tus, wed, thu, fri, sat, sun)
        chart_data = {}
        # Iterate over the activity data and calculate distance and calories
        for activity, date, duration in activity_data:
            
            # set the factors for each activity
            if activity == 'Walking':
                factor_distance = 1.36   # povprečje je 1.36m/s
                factor_calories = 0.0644 # povprečje je 232 kcal/h
            elif activity == 'Running':
                factor_distance = 2.68 # povprečje je 2.68m/s
                factor_calories = 0.20 # povprečje je 725 kcal/h
            elif activity == 'Cycling':
                factor_distance = 8.04 # povprečje je 8.04m/s
                factor_calories = 0.24 # povprečje je 888 kcal/h
            else:
                factor_distance = 0
                factor_calories = 0
            
            activity = activity.lower()
            
            #convert date to day in week
            date = datetime.strptime(date, '%Y-%m-%d').date()
            day = date.strftime('%A')
            
            #add the data to the chart_data
            if day not in chart_data:
                chart_data[day] = {}
            if activity not in chart_data[day]:
                chart_data[day][activity] = {}
            
            #calculate the duration, distance and calories
            chart_data[day][activity]['minutes'] = math.ceil(duration/60)           # in minutes (rounded up)
            chart_data[day][activity]['calories'] = int(duration * factor_calories) # in kcal
            chart_data[day][activity]['distance'] = int(duration * factor_distance) # in meters

        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify(f'Error retrieving weekly data: {str(e)}'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)