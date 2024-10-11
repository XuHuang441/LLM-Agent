import itertools
import json

import openai
from openai import OpenAI
import pandas as pd
import yaml

client = OpenAI()

with open('../util/llm_prompts.yaml', 'r', encoding='utf-8') as file:
    llm_prompts = yaml.safe_load(file)


def get_prompt(name):
    for prompt in llm_prompts['llm_prompts']:
        if prompt['name'] == name:
            return prompt['prompt']
    return None


system_prompt = get_prompt("AI_Eval_System")


def get_comparison(description):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        # This is to enable JSON mode, making sure responses are valid json objects
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": description
            }
        ],
    )

    return response.choices[0].message.content

df = pd.read_csv('../final/output/triples.csv')

for _, row in df[1:2].iterrows():
    gt_abs = row['label']
    df_abs = pd.read_csv('../Abs Generation/output/abstract/abstracts_1.csv')

    dragon = df_abs['dragon'].iloc[0]
    dragon_id = df_abs['dragon_id'].iloc[0]

    rand_abs_list = []

    for _, row_abs in df_abs.iterrows():
        random = row_abs['random']
        random_id = row_abs['random_id']

        rand_abs_list.append({'random_id': random_id, 'random': random})

    abs_list = [{'dragon_id': dragon_id, 'dragon': dragon}] + rand_abs_list

    combinations = list(itertools.combinations(abs_list, 2))

    for pair in combinations[::2]:

        if 'dragon' in pair[0]:

            user_prompt = ("Here is the original abstract for your reference:"
                           f"**Original Abstract:** [{gt_abs}]"
                           "Here are the two abstracts to compare:"
                           f"**Abstract 1:** [{pair[0]['dragon']}]"
                           f"**Abstract 2:** [{pair[1]['random']}]")

            print(f"dragon: {pair[0]['dragon_id']} vs random: {pair[1]['random_id']}")
            response = get_comparison(user_prompt)
            response_dict = json.loads(response)
            print(response_dict["result"])

        # elif 'random' in pair[0]:
        #
        #     user_prompt = ("Here is the original abstract for your reference:"
        #                    f"**Original Abstract:** [{gt_abs}]"
        #                    "Here are the two abstracts to compare:"
        #                    f"**Abstract 1:** [{pair[0]['random']}]"
        #                    f"**Abstract 2:** [{pair[1]['random']}]")
        #
        #     print(f"random: {pair[0]['random_id']} vs random: {pair[1]['random_id']}")
        #     print(get_comparison(user_prompt))
