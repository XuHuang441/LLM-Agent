import ast
import yaml
import pandas as pd
from util.LLMmodule import get_LLM_response

# Load YAML
with open('../util/llm_prompts.yaml', 'r', encoding='utf-8') as file:
    llm_prompts = yaml.safe_load(file)

def get_prompt(name):
    for prompt in llm_prompts['llm_prompts']:
        if prompt['name'] == name:
            return prompt['prompt']
    return None

result_abs = []

triples_file_path = '../final/output/triples.csv'

df = pd.read_csv(triples_file_path)

abs_gen_1 = get_prompt("abs_gen_1")
abs_gen_2 = get_prompt("abs_gen_2")

for index, row in df.iterrows():
    corpus = ast.literal_eval(row['corpus'])
    topic = row['topic']

    title_list = []
    abstract_list = []

    for corpus_dict in corpus:
        for title, abstract in corpus_dict.items():
            title_list.append(title)
            abstract_list.append(abstract)

    content = (f"{abs_gen_1}\nTopic Paragraph:\n{topic}\n\nPrevious Papers' Titles and Abstracts:\n\n"
               f"1. Title: {title_list[0]}\nAbstract: {abstract_list[0]}\n\n"
               f"2. Title: {title_list[1]}\nAbstract: {abstract_list[1]}\n\n"
               f"3. Title: {title_list[2]}\nAbstract: {abstract_list[2]}\n\n"
               f"4. Title: {title_list[3]}\nAbstract: {abstract_list[3]}\n\n"
               f"5. Title: {title_list[4]}\nAbstract: {abstract_list[4]}\n\n"
               f"6. Title: {title_list[5]}\nAbstract: {abstract_list[5]}\n\n"
               f"7. Title: {title_list[6]}\nAbstract: {abstract_list[6]}\n\n"
               f"8. Title: {title_list[7]}\nAbstract: {abstract_list[7]}\n\n"
               f"9. Title: {title_list[8]}\nAbstract: {abstract_list[8]}\n\n"
               f"10. Title: {title_list[9]}\nAbstract: {abstract_list[9]}\n\n"
               f"Instructions: \n{abs_gen_2}")

    # print(get_LLM_response(content))

    result_abs.append(get_LLM_response(content))

df['generated_abs'] = result_abs

df.to_csv('output/gen_abs.csv', index=False)
