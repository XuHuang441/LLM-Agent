"""
convert the abs_gen.csv to a TSV the same format as queries.dev.small.tsv
"""
import os

import pandas as pd

df = pd.read_csv('output/gen_abs.csv')
output_dir = 'output/query'
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():

    tsv_data = []

    topic = row['topic'].replace("\n", " ")

    # print(topic)

    tsv_data.append([0, topic])

    # Convert to DataFrame
    tsv_df = pd.DataFrame(tsv_data)

    # Define the output TSV file path
    tsv_file_path = os.path.join(output_dir, f'query_{index}.tsv')

    # Save the TSV file
    tsv_df.to_csv(tsv_file_path, sep='\t', header=False, index=False)

    break

