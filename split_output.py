import os
import json
import csv
import re

folder_path = 'research_submissions'

def contains_chinese(text):
    """Check if the text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def contains_english(text):
    """Check if the text contains English characters."""
    return bool(re.search(r'[a-zA-Z]', text))

def write_CSV_file(data, output_file, filename, writeHeader):
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'user', 'assistant']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if writeHeader:
            writer.writeheader()
        user = ''
        assistant = ''
        for entry in data['history']:
            for message in entry['messages']:
                if message['role'] == 'user':
                    user += message['content'] + '\n'  # 將user的內容以換行符號結尾
                elif message['role'] == 'assistant':
                    assistant += message['content'] + '\n'  # 將assistant的內容以換行符號結尾
        writer.writerow({'filename': filename, 'user': user, 'assistant': assistant})


if not os.path.exists(folder_path):
    print("error: folder not found")
    exit()

user = []
assistant = []
filenames = sorted(os.listdir(folder_path))
zh_first = True
en_first = True

for idx, filename in enumerate(filenames):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            user = ''
            assistant = ''
            if contains_chinese(data['history'][0]['name']):
                write_CSV_file(data, 'output_zh.csv', filename, zh_first)
                zh_first = False
            elif contains_english(data['history'][0]['name']):
                write_CSV_file(data, 'output_en.csv', filename, en_first)
                en_first = False
            else:
                print(filename)
        