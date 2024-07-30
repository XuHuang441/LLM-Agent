import yaml


with open('llm_prompts.yaml', 'r', encoding='utf-8') as file:
    llm_prompts = yaml.safe_load(file)

def get_prompt(name):
    for prompt in llm_prompts['llm_prompts']:
        if prompt['name'] == name:
            return prompt['prompt']
    return None

greeting_prompt = get_prompt("retriever")
print(greeting_prompt)
