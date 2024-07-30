"""
Get the abstracts of the author's historical papers
"""
from datetime import datetime
from xml.etree import ElementTree
from dateutil import parser
from lxml import etree
import chardet
import requests


def get_latest_paper_abstract(author, date):
    author_query = author.replace(" ", "+")
    url = f"http://export.arxiv.org/api/query?search_query=au:{author_query}&start=0&max_results=300"  # Adjust max_results if needed

    response = requests.get(url)
    papers_list = []

    if response.status_code == 200:

        content = response.content
        detected_encoding = chardet.detect(content)

        try:
            # 直接使用 lxml 解析响应内容
            xmlparser = etree.XMLParser(recover=True, encoding=detected_encoding['encoding'])
            root = etree.fromstring(content, parser=xmlparser)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            # print(entries)
        except etree.XMLSyntaxError as e:
            print(f"XML Syntax Error: {e}")

        total_papers = 0
        data_to_save = []

        papers_by_year = {}

        for entry in entries:

            published_date = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            date_obj = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%SZ')
            if date_obj > date:
                continue

            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            published = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            authors_elements = entry.findall('{http://www.w3.org/2005/Atom}author')
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in authors_elements]
            link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()  # Get the paper link

            # Check if the specified author is exactly in the authors list
            if author in authors:
                # Remove the specified author from the coauthors list for display
                coauthors = [author for author in authors if author != author]
                coauthors_str = ", ".join(coauthors)

                papers_list.append({
                    "date": published,
                    "title": title,
                    "Abstract": abstract,
                    "coauthors": coauthors_str,
                    "link": link  # Add the paper link to the dictionary
                })
            authors_elements = entry.findall('{http://www.w3.org/2005/Atom}author')
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in authors_elements]

            if author in authors:
                # print(author)
                # print(authors)
                total_papers += 1
                published_date = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
                date_obj = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%SZ')

                year = date_obj.year
                if year not in papers_by_year:
                    papers_by_year[year] = []
                papers_by_year[year].append(entry)

        if total_papers > 40:
            for cycle_start in range(min(papers_by_year), max(papers_by_year) + 1, 5):
                cycle_end = cycle_start + 4
                for year in range(cycle_start, cycle_end + 1):
                    if year in papers_by_year:
                        selected_papers = papers_by_year[year][:2]
                        for paper in selected_papers:
                            title = paper.find('{http://www.w3.org/2005/Atom}title').text.strip()
                            abstract = paper.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                            authors_elements = paper.findall('{http://www.w3.org/2005/Atom}author')
                            co_authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in
                                          authors_elements if
                                          author.find('{http://www.w3.org/2005/Atom}name').text != author]

                            papers_list.append({
                                "Author": author,
                                "title": title,
                                "Abstract": abstract,
                                "Date Period": f"{year}",
                                "Cycle": f"{cycle_start}-{cycle_end}",
                                "Co_author": ", ".join(co_authors)
                            })

        # Trim the list to the 10 most recent papers
        papers_list = papers_list[:10]

        abs_list = []

        for paper in papers_list:
            abs_dic = {paper["title"]: paper["Abstract"]}
            abs_list.append(abs_dic)

        return abs_list

def check_num_papers(author, date):
    author_query = author.replace(" ", "+")
    url = f"http://export.arxiv.org/api/query?search_query=au:{author_query}&start=0&max_results=300"  # Adjust max_results if needed

    response = requests.get(url)

    if response.status_code == 200:
        content = response.content
        detected_encoding = chardet.detect(content)

        try:
            # 直接使用 lxml 解析响应内容
            xmlparser = etree.XMLParser(recover=True, encoding=detected_encoding['encoding'])
            root = etree.fromstring(content, parser=xmlparser)
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            # print(entries)
        except etree.XMLSyntaxError as e:
            print(f"XML Syntax Error: {e}")

        total_papers = 0

        for entry in entries:

            authors_elements = entry.findall('{http://www.w3.org/2005/Atom}author')
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in authors_elements]

            if author in authors:
                # print(author)
                # print(authors)

                published_date = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
                date_obj = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%SZ')

                if date_obj < date:
                    total_papers += 1

        print(total_papers)

        return total_papers
