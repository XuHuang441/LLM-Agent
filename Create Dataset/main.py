from datasets import load_dataset
from retriever import content2topic
from dateutil import parser
from corpus import get_latest_paper_abstract, check_num_papers
import pandas as pd

ds = load_dataset("AcademicEval/AcademicEval", "abs_9K")

data = ds['test']

df_list = []

k = 10

num_iter = len(data)

for entry, _ in zip(data, range(num_iter)):

    result = dict()

    published_date = parser.parse(entry['published'])
    authors = entry['authors']
    author_list = [author.strip() for author in authors.split(', ')]
    title = entry['title']

    num = 0

    for author in author_list:
        num = check_num_papers(author, published_date)
        if num > k:
            latest_abstract = get_latest_paper_abstract(author, published_date)

            result['label'] = entry['abstract']
            result['corpus'] = latest_abstract
            result['topic'] = content2topic(entry['main_content'])

            df_list.append(result)

        break # We don't consider coauthors at the moment


df = pd.DataFrame(df_list)

df.to_csv('output/triples.csv', index=False)

