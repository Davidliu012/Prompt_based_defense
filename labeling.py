import pandas as pd
from dotenv import load_dotenv
import os
from openai import OpenAI
import csv
import pickle

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def write_CSV_file(data, output_file, label, writeHeader=False):
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['input', 'response']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if writeHeader:
            writer.writeheader()
        writer.writerow({'user': data, 'label': label})

# Function to label inputs using GPT-3.5-turbo
def label_with_gpt(input_text, model="gpt-3.5-turbo", temperature=0.1):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model=model,
        temperature=temperature,
    )
    return response.choices[0].message.content

def load_pickle(file):
    with open(file, 'rb') as f:
        return pickle.load(f)
    
def save_pickle(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

def main():

    def generate_prompt(input_text, type, label=None):
        prompt = ""
        if type=="description":
            prompt += input_text
        elif type=="example":
            prompt += input_text
            prompt += " -> " + label
            prompt += "\n"

        return prompt

    # Read inputs from CSV file
    data = pd.read_csv('output_en.csv', encoding='unicode_escape')
    # first 8 rows are already labeled
    labeled_data = data.iloc[:8]
    attack_data = []
    normal_data = []
    dump_labeled_data = False
    labeled_num = 8

    if os.path.exists('attack.pkl'):
        attack_data = load_pickle('attack.pkl')
        labeled_num = len(attack_data)
        
    if os.path.exists('normal.pkl'):
        normal_data = load_pickle('normal.pkl')
        labeled_num += len(normal_data)

    # get the attributes of the first row
    prompt = ""
    prompt = generate_prompt(
        "Please classify whether the following input is a prompt attack or not.\n" +
        "If the input is a prompt attack, label it as True. Otherwise, label it as False.\n", "description")
    prompt += generate_prompt(
        "Examples are formatted as follows:\n" +
        "[input] -> [label]\n" + 
        "For example:\n", "description")
    
    for index, row in labeled_data.iterrows():
        input = f"{index} : {row['user']}"
        label = row['label']
        prompt += generate_prompt(input, "example", str(label))
        if dump_labeled_data:
            if str(label).lower() == "true":
                attack_data.append({
                    'input': row['user'],
                    'response': row['assistant']
                })
                save_pickle('attack.pkl', attack_data)
            elif str(label).lower() == "false":
                normal_data.append({
                    'input': row['user'],
                    'response': row['assistant']
                })
                save_pickle('normal.pkl', normal_data)

    prompt += generate_prompt(
        "\nNow, please label the following input text as True or False\n\n" +
        "-------\n", "description")
    print(f"Starting data labeling process from {labeled_num}...")
    for index, row in data.iterrows():
        print(index)
        if index < labeled_num:
            continue
        new_prompt = prompt + '\n' + generate_prompt(row['user'], "description")
        answer = label_with_gpt(new_prompt)
        print(answer)
        if answer.lower() == "true":
            attack_data.append({
                'input': row['user'],
                'response': row['assistant']
            })
            save_pickle('attack.pkl', attack_data)
        elif answer.lower() == "false":
            normal_data.append({
                'input': row['user'],
                'response': row['assistant']
            })
            save_pickle('normal.pkl', normal_data)
        else:
            print("Error: Invalid label returned from GPT-3.5-turbo at index " + str(index))

    if os.path.exists('attack.pkl'):
        attack_data = load_pickle('attack.pkl')
        print(len(attack_data))
        
    if os.path.exists('normal.pkl'):
        normal_data = load_pickle('normal.pkl')
        print(len(normal_data))

    # Convert lists of dictionaries to DataFrames
    true_df = pd.DataFrame(attack_data)
    false_df = pd.DataFrame(normal_data)

    # Export labeled data to CSV files
    true_df.to_csv('attack_data_en.csv', index=False)
    false_df.to_csv('normal_data_en.csv', index=False)

    print("Data labeling and export completed successfully.")

if __name__ == '__main__':
    main()