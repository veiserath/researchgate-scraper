import time
from bs4 import BeautifulSoup
import requests
import json
from lxml import etree
import psycopg2

import DatabaseCredentials

URL = "https://www.researchgate.net/publication/220591356_Identifying_Software_Project_Risks_An_International_Delphi_Study"
REQUEST = requests.get(URL)
PARSER = "html.parser"
SOUP = BeautifulSoup(REQUEST.text, PARSER)
DOM = etree.HTML(str(SOUP))

con = psycopg2.connect(database=DatabaseCredentials.DATABASE, user=DatabaseCredentials.USER,
                       password=DatabaseCredentials.PASSWORD, host=DatabaseCredentials.HOST,
                       port=DatabaseCredentials.PORT)
print("Database opened successfully")


def create_database():
    with con.cursor() as cursor:
        cursor.execute(open("Database_Model.sql", "r").read())
        con.commit()
        print("Created database")


def insert_article_to_database(title, url, date, publisher, citation_count=None, reference_count=None):
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO ARTICLE (TITLE,URL,DATE,PUBLISHER, CITATION_COUNT, REFERENCE_COUNT) VALUES "
            "(%(title)s, %(url)s, (TO_DATE(%(date)s,'YYYY-MM-DD')), %(publisher)s,%(citation_count)s,%(reference_count)s)",
            {'title': title, 'url': url, 'date': date, 'publisher': publisher, 'citation_count': citation_count,
             'reference_count': reference_count})
        con.commit()
        print("Record inserted successfully")
    except psycopg2.errors.UniqueViolation:
        print("Article was already added!")


def insert_reference_to_database(title, url, date, publisher, main_article_url, reference_url):
    cur = con.cursor()
    insert_article_to_database(title, url, date, publisher)

    cur.execute(
        "INSERT INTO ARTICLEREFERENCE (main_article_url,reference_article_url) "
        "VALUES (%(main_article_url)s,%(reference_url)s)",
        {'main_article_url': main_article_url, 'reference_url': reference_url})


def insert_citation_to_database(article_url_to_insert, citation_url_to_insert):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO ARTICLECITATION (article_id,citation_id) VALUES (article_id_to_insert,citation_id_to_insert)")


def get_count(string):
    count = ""
    for item in string:
        if item.isdigit():
            count += item
    return count


def generate_tree_schema():
    # use get references
    output = "digraph G {"
    output += "\n"
    output += "{ "
    for item in result["citation"]:
        output += '"'
        output += item["headline"]
        output += '"'
        output += "; "

    output += "}"
    output += " -> "
    output += '"'
    output += result["headline"]
    output += '"'
    output += "\n"

    output += result["headline"]
    output += " -> "
    output += "{"
    for citation in get_citations():
        output += '"'
        output += citation["title"]
        output += '"'
        output += "; "
    output += "}"
    output += "\n"
    output += "}"

    with open("graph1.gv", "w") as outfile:
        outfile.write(output)

    return output


def get_reference_article_citation_count(url):
    time.sleep(2)
    request = requests.get(url)
    parser = "html.parser"
    soup = BeautifulSoup(request.text, parser)
    dom = etree.HTML(str(soup))
    citation = str(dom.xpath("//div[contains(text(),'Citations')]/text()")[0])
    return get_count(citation)


def get_citation_count():
    citation = str(DOM.xpath("//div[contains(text(),'Citations')]/text()")[0])
    return get_count(citation)


def get_references_count():
    references = str(DOM.xpath("//div[contains(text(),'References')]/text()")[0])
    return get_count(references)


def get_ld_json() -> dict:
    return json.loads("".join(SOUP.find("script", {"type": "application/ld+json"}).contents))


def export_to_pdf():
    title = result["headline"]
    url = result["mainEntityOfPage"]
    date = result["datePublished"]
    publisher = result["publisher"]["name"]
    citation_count = get_citation_count()
    reference_count = get_references_count()
    references = get_references()
    citations = get_citations()

    paper_info = {
        'title': title,
        'url': url,
        'date': date,
        'publisher': publisher,
        'citation count': citation_count,
        'reference count': reference_count,
        'references': references,
        'citations': citations
    }
    result_json = json.dumps(paper_info)

    insert_article_to_database(title, url, date, publisher, citation_count, reference_count)

    for item in references:
        insert_reference_to_database(item["title"],item["url"],item["date"],item["publisher"],url, item["url"])
    with open("result.json", "w") as outfile:
        outfile.write(result_json)


def print_main_article_metadata():
    print(result["headline"])
    print(result["datePublished"])
    print(result["mainEntityOfPage"])
    # make it a one-liner
    for item in result["author"]:
        print(item["name"])
    print(result["publisher"]["name"])
    print("====")


def get_references():
    references = []
    i = 0
    for item in result["citation"]:
        if i >= citations_range:
            break
        paper_info = {
            'title': item["headline"],
            'url': item["mainEntityOfPage"],
            'date': item["datePublished"],
            'publisher': item["publisher"]["name"],
        }
        references.append(paper_info)
        i += 1
    return references


def get_citations():
    citations = []
    for i in range(citations_range, len(result["citation"])):
        paper_info = {
            'title': result["citation"][i]["headline"],
            'url': result["citation"][i]["mainEntityOfPage"],
            'date': result["citation"][i]["datePublished"],
            'publisher': result["citation"][i]["publisher"]["name"],
        }
        citations.append(paper_info)
    return citations


def print_references():
    i = 0
    for item in result["citation"]:
        print(i)
        print(item["headline"])
        print(item["datePublished"])
        print(item["mainEntityOfPage"])
        # make it a one-liner
        for subitem in item["author"]:
            print(subitem["name"])
        print(item["publisher"]["name"])
        i += 1
        print("===")


# create_database()
# insert_article_to_database('title_function', 'url_from_hell', '2006-01-01', 'kacprowski', 10, 200)

# get_citation_count()
result = get_ld_json()
#
citations_range = len(result["citation"]) - 1 - len(get_citation_count())
print_main_article_metadata()
print_references()
export_to_pdf()
# print(generate_tree_schema())


con.close()
