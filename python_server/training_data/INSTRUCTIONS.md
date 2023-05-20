THIS FOLDER CONTAINS THE TRAINING DATA FOR THE MODEL
each .csv file is data for a specific activity
the data contains x, y, z values for accelerometer and gyroscope the lable is also added.

The RandomForestClassifier is used to train the model to recognize the activity of walking, running ad cycling.
For training the model, the data from all 3 files should be used together.

```


Data: [
{'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Running', 'duration': 1},
{'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Running', 'duration': 1},
{'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Running', 'duration': 1},
{'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Running', 'duration': 1}]
```

[{'avg_acc_x_1': -0.0076335879999999984, 'avg_acc_y_1': -0.0076335879999999984, 'avg_acc_z_1': -0.0076335879999999984, 'label_1': 'Walking', 'avg_acc_x_2': -0.0076335879999999984, 'avg_acc_y_2': -0.0076335879999999984, 'avg_acc_z_2': -0.0076335879999999984, 'label_2': 'Walking', 'avg_acc_x_3': -0.0076335879999999984, 'avg_acc_y_3': -0.0076335879999999984, 'avg_acc_z_3': -0.0076335879999999984, 'label_3': 'Walking', 'avg_acc_x_4': -0.0076335879999999984, 'avg_acc_y_4': -0.0076335879999999984, 'avg_acc_z_4': -0.0076335879999999984, 'label_4': 'Walking', 'avg_acc_x_5': -0.0076335879999999984, 'avg_acc_y_5': -0.0076335879999999984, 'avg_acc_z_5': -0.0076335879999999984, 'label_5': 'Walking', 'avg_acc_x_6': -0.0076335879999999984, 'avg_acc_y_6': -0.0076335879999999984, 'avg_acc_z_6': -0.0076335879999999984, 'label_6': 'Walking', 'avg_acc_x_7': -0.0076335879999999984, 'avg_acc_y_7': -0.0076335879999999984, 'avg_acc_z_7': -0.0076335879999999984, 'label_7': 'Walking', 'avg_acc_x_8': -0.0076335879999999984, 'avg_acc_y_8': -0.0076335879999999984, 'avg_acc_z_8': -0.0076335879999999984, 'label_8': 'Walking', 'avg_acc_x_9': -0.0076335879999999984, 'avg_acc_y_9': -0.0076335879999999984, 'avg_acc_z_9': -0.0076335879999999984, 'label_9': 'Walking', 'avg_acc_x_10': -0.0076335879999999984, 'avg_acc_y_10': -0.0076335879999999984, 'avg_acc_z_10': -0.0076335879999999984, 'label_10': 'Walking'},
{'avg_acc_x_1': -0.0076335879999999984, 'avg_acc_y_1': -0.0076335879999999984, 'avg_acc_z_1': -0.0076335879999999984, 'label_1': 'Walking', 'avg_acc_x_2': -0.0076335879999999984, 'avg_acc_y_2': -0.0076335879999999984, 'avg_acc_z_2': -0.0076335879999999984, 'label_2': 'Walking', 'avg_acc_x_3': -0.0076335879999999984, 'avg_acc_y_3': -0.0076335879999999984, 'avg_acc_z_3': -0.0076335879999999984, 'label_3': 'Walking', 'avg_acc_x_4': -0.0076335879999999984, 'avg_acc_y_4': -0.0076335879999999984, 'avg_acc_z_4': -0.0076335879999999984, 'label_4': 'Walking', 'avg_acc_x_5': -0.0076335879999999984, 'avg_acc_y_5': -0.0076335879999999984, 'avg_acc_z_5': -0.0076335879999999984, 'label_5': 'Walking', 'avg_acc_x_6': -0.0076335879999999984, 'avg_acc_y_6': -0.0076335879999999984, 'avg_acc_z_6': -0.0076335879999999984, 'label_6': 'Walking', 'avg_acc_x_7': -0.0076335879999999984, 'avg_acc_y_7': -0.0076335879999999984, 'avg_acc_z_7': -0.0076335879999999984, 'label_7': 'Walking', 'avg_acc_x_8': -0.0076335879999999984, 'avg_acc_y_8': -0.0076335879999999984, 'avg_acc_z_8': -0.0076335879999999984, 'label_8': 'Walking', 'avg_acc_x_9': -0.0076335879999999984, 'avg_acc_y_9': -0.0076335879999999984, 'avg_acc_z_9': -0.0076335879999999984, 'label_9': 'Walking', 'avg_acc_x_10': -0.0076335879999999984, 'avg_acc_y_10': -0.0076335879999999984, 'avg_acc_z_10': -0.0076335879999999984, 'label_10': 'Walking'},
{'avg_acc_x_1': -0.0076335879999999984, 'avg_acc_y_1': -0.0076335879999999984, 'avg_acc_z_1': -0.0076335879999999984, 'label_1': 'Walking', 'avg_acc_x_2': -0.0076335879999999984, 'avg_acc_y_2': -0.0076335879999999984, 'avg_acc_z_2': -0.0076335879999999984, 'label_2': 'Walking', 'avg_acc_x_3': -0.0076335879999999984, 'avg_acc_y_3': -0.0076335879999999984, 'avg_acc_z_3': -0.0076335879999999984, 'label_3': 'Walking', 'avg_acc_x_4': -0.0076335879999999984, 'avg_acc_y_4': -0.0076335879999999984, 'avg_acc_z_4': -0.0076335879999999984, 'label_4': 'Walking'}]

model data
[DEBUG] combined data: {'avg_acc_x_0': 0.0839694649, 'avg_acc_y_0': 0.5793893098999999, 'avg_acc_z_0': -0.2312977109, 'duration_0': 0.5, 'avg_acc_x_1': 0.1259541997, 'avg_acc_y_1': 0.5625954299, 'avg_acc_z_1': -0.2068702274, 'duration_1': 0.5, 'avg_acc_x_2': 0.0374045802, 'avg_acc_y_2': 0.551145047, 'avg_acc_z_2': -0.22137405029999999, 'duration_2': 0.5, 'avg_acc_x_3': 0.060305344, 'avg_acc_y_3': 0.5129770964, 'avg_acc_z_3': -0.3152671787, 'duration_3': 0.5, 'avg_acc_x_4': 0.1061068714, 'avg_acc_y_4': 0.5793893217000001, 'avg_acc_z_4': -0.29007633560000007, 'duration_4': 0.5, 'avg_acc_x_5': 0.031297711000000006, 'avg_acc_y_5': 0.5312977134000001, 'avg_acc_z_5': -0.3564885513, 'duration_5': 0.5, 'avg_acc_x_6': 0.0648854968, 'avg_acc_y_6': 0.5366412252000001, 'avg_acc_z_6': -0.2625954212, 'duration_6': 0.5, 'avg_acc_x_7': 0.1511450373, 'avg_acc_y_7': 0.5106870293, 'avg_acc_z_7': -0.2511450377000001, 'duration_7': 0.5, 'avg_acc_x_8': 0.09770992540000002, 'avg_acc_y_8': 0.5244274884, 'avg_acc_z_8': -0.30534351179999997, 'duration_8': 0.5, 'avg_acc_x_9': 0.08931297539999998, 'avg_acc_y_9': 0.5549618335, 'avg_acc_z_9': -0.22748091889999994, 'duration_9': 0.5, 'avg_gyro_x_0': -0.008876949500000002, 'avg_gyro_y_0': 0.015568845000000001, 'avg_gyro_z_0': -0.0178833007, 'avg_gyro_x_1': -0.0179101528, 'avg_gyro_y_1': 0.005314938799999999, 'avg_gyro_z_1': 0.0011596680999999998, 'avg_gyro_x_2': -0.015224605900000002, 'avg_gyro_y_2': -0.0012768583999999991, 'avg_gyro_z_2': -0.012268066400000001, 'avg_gyro_x_3': -0.018886715300000002, 'avg_gyro_y_3': 0.0018969699000000006, 'avg_gyro_z_3': -0.0288696289, 'avg_gyro_x_4': -0.015468746500000002, 'avg_gyro_y_4': 0.0067797822999999995, 'avg_gyro_z_4': -0.04205322239999999, 'avg_gyro_x_5': -0.017666012, 'avg_gyro_y_5': -0.0024975614999999994, 'avg_gyro_z_5': -0.051818847700000004, 'avg_gyro_x_6': -0.009365230799999999, 'avg_gyro_y_6': 0.0023852511999999998, 'avg_gyro_z_6': -0.027893066400000006, 'avg_gyro_x_7': -0.0237695277, 'avg_gyro_y_7': 0.012883297799999999, 'avg_gyro_z_7': -0.0440063477, 'avg_gyro_x_8': -0.0264550746, 'avg_gyro_y_8': 0.0084887668, 'avg_gyro_z_8': -0.027893066400000006, 'avg_gyro_x_9': -0.016445308999999998, 'avg_gyro_y_9': 0.0121508762, 'avg_gyro_z_9': -0.017395019399999996}

    {
    "Monday": {
        "running": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        },
        "cycling": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        },
        "walking": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        }
    },
    "Tuseday": {
        "running": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        },
        "cycling": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        },
        "walking": {
        "minutes": 100,
        "calories": 500,
        "distance": 1000
        }
    }
    }
