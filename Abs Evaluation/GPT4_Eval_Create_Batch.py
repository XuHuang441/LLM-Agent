import itertools
import json

import openai
from openai import OpenAI
import pandas as pd
import yaml


with open('../util/llm_prompts.yaml', 'r', encoding='utf-8') as file:
    llm_prompts = yaml.safe_load(file)

def get_prompt(name):
    for prompt in llm_prompts['llm_prompts']:
        if prompt['name'] == name:
            return prompt['prompt']
    return None


system_prompt = get_prompt("AI_Eval_System")

tasks = []

df = pd.read_csv('../final/output/triples.csv')

for i, row in df[1:20].iterrows():
    gt_abs = row['label']
    df_abs = pd.read_csv(f'../Abs Generation/output/abstract/abstracts_{i}.csv')

    dragon = df_abs['dragon'].iloc[0]
    dragon_id = df_abs['dragon_id'].iloc[0]

    rand_abs_list = []

    for _, row_abs in df_abs.iterrows():
        random = row_abs['random']
        random_id = row_abs['random_id']

        rand_abs_list.append({'random_id': random_id, 'random': random})

    abs_list = [{'dragon_id': dragon_id, 'dragon': dragon}] + rand_abs_list

    combinations = list(itertools.combinations(abs_list, 2))

    for pair in combinations:

        if 'dragon' in pair[0]:

            user_prompt = ("Here is the original abstract for your reference:"
                           f"**Original Abstract:** [{gt_abs}]"
                           "Here are the two abstracts to compare:"
                           f"**Abstract 1:** [{pair[0]['dragon']}]"
                           f"**Abstract 2:** [{pair[1]['random']}]")

            task = {
                "custom_id": f"dragon: {pair[0]['dragon_id']} vs random: {pair[1]['random_id']}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    # This is what you would have in your Chat Completions API call
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "response_format": {
                        "type": "json_object"
                    },
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                }
            }

        elif 'random' in pair[0]:

            user_prompt = ("Here is the original abstract for your reference:"
                           f"**Original Abstract:** [{gt_abs}]"
                           "Here are the two abstracts to compare:"
                           f"**Abstract 1:** [{pair[0]['random']}]"
                           f"**Abstract 2:** [{pair[1]['random']}]")

            task = {
                "custom_id": f"random: {pair[0]['random_id']} vs random: {pair[1]['random_id']}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    # This is what you would have in your Chat Completions API call
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "response_format": {
                        "type": "json_object"
                    },
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                }
            }

        tasks.append(task)

# Creating the file

file_name = "data/batch_tasks_eval.jsonl"

with open(file_name, 'w') as file:
    for obj in tasks:
        file.write(json.dumps(obj) + '\n')
