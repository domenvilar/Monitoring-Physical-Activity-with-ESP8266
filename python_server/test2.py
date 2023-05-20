import math
from datetime import datetime, timedelta
import statistics as stat
from scipy.signal import find_peaks
from scipy.stats import pearsonr
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from joblib import load
import logging
import csv
import sqlite3
from sklearn.model_selection import train_test_split
import pandas as pd
import sqlite3



conn = sqlite3.connect('database.db')
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
activity_data = cursor.fetchall() # [(activity, date, sum_duration), ...] ???

# print(activity_data)

# format the data for the chart
chart_data = {}
for activity, date, duration in activity_data:

    if activity == 'Walking':
        factor_distance = 1.36   # kao da je 1.36m/s
        factor_calories = 0.0644 # kao je 232 kcal/h
    elif activity == 'Running':
        factor_distance = 2.68 # kao da je 2.68m/s
        factor_calories = 0.20 # kao da je 725 kcal/h
    elif activity == 'Cycling':
        factor_distance = 8.04 # kao da je 8.04m/s
        factor_calories = 0.24 # kao da je 888 kcal/h
    

    activity = activity.lower()
    date = datetime.strptime(date, '%Y-%m-%d').date()
    day = date.strftime('%A')

    if day not in chart_data:
        chart_data[day] = {}
    if activity not in chart_data[day]:
        chart_data[day][activity] = {}
    

    chart_data[day][activity]['minutes'] = math.ceil(duration/60)
    chart_data[day][activity]['calories'] = int(duration * factor_calories)
    chart_data[day][activity]['distance'] = int(duration * factor_distance)

print(chart_data)
