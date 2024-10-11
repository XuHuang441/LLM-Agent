import json
import pandas as pd

result_file_name = "output/batch_ShIyhTAPmWpHJ9PQwXV394JE_output.jsonl"

results = []
with open(result_file_name, 'r') as file:
    for line in file:
        # Parsing the JSON string into a dict and appending to the list of results
        json_object = json.loads(line.strip())
        results.append(json_object)

print(len(results))

# Reading only the first results
for res in results[:1]:
    print(res)
    result = res['response']['body']['choices'][0]['message']['content']
    print(result)