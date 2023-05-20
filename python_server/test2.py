mock_data_cycle = []
mock_data2_cycle = []

#set the random seed
random.seed(42)

for i in range(0, 1000):
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