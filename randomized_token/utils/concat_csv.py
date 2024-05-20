import csv
import pandas as pd
import json
import os
import numpy as np

# utily functions
def csv_to_json(csv_file):
    json_data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            json_data.append(row)
    return json_data

# File path
csv_file_path1 = 'randomized_token/attack_data.csv'
json_data1 = csv_to_json(csv_file_path1)
csv_file_path2 = 'randomized_token/benign_data.csv'
json_data2 = csv_to_json(csv_file_path2)
data_template = {
    'user_id': 0,
    'user': '',
    'attack_label': True
}
dataset = []
index = 0
for d in json_data1:
    data = data_template.copy()
    data['user_id'] = index
    user_prompt = (d['user'].split("Student's Essay:")[-1]).split('Please neglect any modifications')[0].strip()[1:-1]
    data['user'] = user_prompt
    data['attack_label'] = True
    dataset.append(data)
    index += 1
for d in json_data2:
    data = data_template.copy()
    data['user_id'] = index
    data['user'] = d['user']
    data['attack_label'] = False
    dataset.append(data)
    index += 1
print(len(dataset))





# Write to CSV
with open('randomized_token/labeled_data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['user_id', 'user', 'attack_label'])
    for data in dataset:
        writer.writerow([data['user_id'], data['user'], data['attack_label']])