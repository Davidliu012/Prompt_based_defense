import csv
import pandas as pd
import json

# Function to read CSV and convert to JSON
def csv_to_json(csv_file):
    json_data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            json_data.append(row)
    return json_data

# File path
csv_file_path = 'output_en.csv'

# Convert CSV to JSON
json_data = csv_to_json(csv_file_path)

data_with_attack = []
for data in json_data:
    final_score = data['assistant'].split('Final score:')[-1]
    if '10/10' in final_score:
        data_with_attack.append(data)

# print number of data with attack
print(len(data_with_attack))

# Write to CSV
with open('human_labeled_dataset/attack_data_en.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['filename', 'user', 'assistant'])
    for data in data_with_attack:
        writer.writerow([data['filename'], data['user'], data['assistant']])