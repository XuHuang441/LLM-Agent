"""
convert the abs_gen.csv to a TSV the same format as collection.tsv
"""
import os

import pandas as pd
import ast

df = pd.read_csv('output/gen_abs.csv')
output_dir = 'output/collection'
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():

    tsv_data = []

    temp_list = ast.literal_eval(row['corpus'])

    i = 0
    for abs_dict in temp_list:
        for title, abstract in abs_dict.items():
            title = title.replace('\n', ' ')
            abstract = abstract.replace('\n', ' ')
            tsv_data.append([i, abstract, title])

        i += 1

    # Convert to DataFrame
    tsv_df = pd.DataFrame(tsv_data, columns=['id', 'text', 'title'])

    # Define the output TSV file path
    tsv_file_path = os.path.join(output_dir, f'collection_{index}.tsv')

    # Save the TSV file
    tsv_df.to_csv(tsv_file_path, sep='\t', index=False)

    break

