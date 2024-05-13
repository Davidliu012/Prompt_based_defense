import csv
import pandas as pd
import json
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
import random
from tqdm import tqdm

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def generate_chat_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=temperature,
    )
    return response.choices[0].message.content

num_benign_data = 100
# https://chat.openai.com/share/2aed1e39-907b-4359-8883-e7e6ac0192c2
# 1. Tone - Formal, Informal
# 2. Perspective - Objective, Subjective
# 3. Depth - Comprehensive, Surface-level
# 4. Language - Technical, Layman's terms
# 5. Structure - Linear, Non-linear
# 6. Voice - Authoritative, Conversational
# 7. Complexity - Simple, Complex
# 8. Style - Descriptive, Concise
# 9. Focus - Narrow, Broad
# 10. Intensity - High, Low
# 11. Originality - Innovative, Derivative
# 12. Research - Rigorous, Sparse
# 13. Credibility - Reliable, Questionable
# 14. Engagement - Captivating, Boring
# 15. Depth of Analysis - In-depth, Superficial
# 16. Objectivity - Impartial, Biased
# 17. Timeliness - Current, Outdated
# 18. Accessibility - Clear, Confusing
# 19. Emotionality - Emotional, Detached
# 20. Relevance - Timely, Irrelevant
article_attribute = [
    'Tone', 'Perspective', 'Depth', 'Language', 'Structure', 'Voice', 'Complexity', 'Style', 'Focus', 'Intensity',
    'Originality', 'Research', 'Credibility', 'Engagement', 'Depth of Analysis', 'Objectivity', 'Timeliness',
    'Accessibility', 'Emotionality', 'Relevance'
]
attribute_value = {
    'Tone': ["Formal", "Informal"],
    'Perspective': ["Objective", "Subjective"],
    'Depth': ["Comprehensive", "Surface-level"],
    'Language': ["Technical", "Layman's terms"],
    'Structure': ["Linear", "Non-linear"],
    'Voice': ["Authoritative", "Conversational"],
    'Complexity': ["Simple", "Complex"],
    'Style': ["Descriptive", "Concise"],
    'Focus': ["Narrow", "Broad"],
    'Intensity': ["High", "Low"],
    'Originality': ["Innovative", "Derivative"],
    'Research': ["Rigorous", "Sparse"],
    'Credibility': ["Reliable", "Questionable"],
    'Engagement': ["Captivating", "Boring"],
    'Depth of Analysis': ["In-depth", "Superficial"],
    'Objectivity': ["Impartial", "Biased"],
    'Timeliness': ["Current", "Outdated"],
    'Accessibility': ["Clear", "Confusing"],
    'Emotionality': ["Emotional", "Detached"],
    'Relevance': ["Timely", "Irrelevant"]
}
num_words_range = [300, 400, 500, 600]

num_attribute_each_article = 8
data_template = {
    'user_index': 0,
    'user': '',
}
dataset = []
for i in tqdm(range(num_benign_data)):
    # use tqdm
    data = data_template.copy()
    data['user_index'] = i
    article_gen_prompt = """Please generate an article that presents the statement "Do you agree or disagree with the statement that Artificial Intelligence will eventually replace humans in most areas of work in the future world.\nFurthermore, you should present the article based on the following properties:\n"""
    attributes = random.sample(article_attribute, num_attribute_each_article)
    # use enumerate:
    for i, attribute in enumerate(attributes):
        article_gen_prompt += f"{i + 1}. A {random.choice(attribute_value[attribute])} {attribute}\n"
    num_words = random.choice(num_words_range)
    article_gen_prompt += f"Please generate an article with around {num_words} words."   
    article = generate_chat_completion(article_gen_prompt)
    data['user'] = article
    dataset.append(data)

# Write to CSV
with open('benign_data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['user_index', 'user'])
    for data in dataset:
        writer.writerow([data['user_index'], data['user']])