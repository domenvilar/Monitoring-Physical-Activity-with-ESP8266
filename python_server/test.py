import csv
import random


data_acc = [{'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'},
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}, 
        {'avg_acc_x': -0.0076335879999999984, 'avg_acc_y': -0.0076335879999999984, 'avg_acc_z': -0.0076335879999999984, 'label': 'Walking'}]

data_gyro= [{'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}, 
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'},
        {'avg_gyro_x': 0.0, 'avg_gyro_y': 0.0, 'avg_gyro_z': 0.0, 'label': 'Walking'}]


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

    # add the label back to the dictionary
    
    return merged_data

def merge_acc_gyro(acc_data, gyro_data):

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

mock_data_walk = []
mock_data2_walk = []

# set the random seed 
random.seed(11)

for i in range(0, 1000):
    random_num = random.randint(0, 100)
    random_num2 = random.randint(0, 100)
    random_num3 = random.randint(0, 100)
    random_krat = random.randint(0, 1)
    mock_data_walk.append({'avg_gyro_x': random_num, 'avg_gyro_y': random_num2, 'avg_gyro_z': random_num3, 'label': 'Walking'})
    mock_data2_walk.append({'avg_gyro_x': random_num*random_krat, 'avg_gyro_y': random_num2*random_krat, 'avg_gyro_z': random_num3*random_krat, 'label': 'Walking'})


mockcombined_walking = merge_acc_gyro(mock_data_walk, mock_data2_walk)
label = mockcombined_walking[0]['label']

file_name = f'data_test_{label}.csv'

with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(mockcombined_walking[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mockcombined_walking)


# ?=================================================================================================

mock_data_run = []
mock_data2_run = []

#set the random seed
random.seed(42)

for i in range(0, 1000):
    random_num = random.randint(0, 100)
    random_num2 = random.randint(0, 100)
    random_num3 = random.randint(0, 100)
    random_krat = random.randint(0, 1)
    mock_data_run.append({'avg_gyro_x': random_num, 'avg_gyro_y': random_num2, 'avg_gyro_z': random_num3, 'label': 'Running'})
    mock_data2_run.append({'avg_gyro_x': random_num*random_krat, 'avg_gyro_y': random_num2*random_krat, 'avg_gyro_z': random_num3*random_krat, 'label': 'Running'})


mockcombined_run = merge_acc_gyro(mock_data_run, mock_data2_run)
label = mockcombined_run[0]['label']

file_name = f'data_test_{label}.csv'

with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(mockcombined_run[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mockcombined_run)

# ?=================================================================================================
mock_data_cycle = []
mock_data2_cycle = []

#set the random seed
random.seed(104)

for i in range(0, 50000):
    random_num = random.randint(0, 100)
    random_num2 = random.randint(0, 100)
    random_num3 = random.randint(0, 100)
    random_krat = random.randint(0, 1)
    mock_data_cycle.append({'avg_gyro_x': random_num, 'avg_gyro_y': random_num2, 'avg_gyro_z': random_num3, 'label': 'Cycling'})
    mock_data2_cycle.append({'avg_gyro_x': random_num*random_krat, 'avg_gyro_y': random_num2*random_krat, 'avg_gyro_z': random_num3*random_krat, 'label': 'Cyckling'})


mockcombined_cycle = merge_acc_gyro(mock_data_cycle, mock_data2_cycle)
label = mockcombined_cycle[0]['label']

file_name = f'data_test_{label}.csv'

with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(mockcombined_cycle[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mockcombined_cycle)