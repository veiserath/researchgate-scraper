from bs4 import BeautifulSoup
import requests
import json
from lxml import etree

url = "https://www.researchgate.net/publication/346429437_Optimizing_clinical_research_procedures_in_public_health_emergencies"
request = requests.get(url)
parser = "html.parser"
soup = BeautifulSoup(request.text, parser)


def get_citation_count():
    dom = etree.HTML(str(soup))
    citation = str(dom.xpath("//div[contains(text(),'Citations')]/text()")[0])
    # references = str(dom.xpath("//div[contains(text(),'References')]/text()")[0])
    return citation


def get_ld_json() -> dict:
    return json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))


def print_main_article_metadata():
    print(result["headline"])
    print(result["datePublished"])
    print(result["mainEntityOfPage"])
    # make it a one-liner
    for item in result["author"]:
        print(item["name"])
    print(result["publisher"]["name"])
    print("====")


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


get_citation_count()
result = get_ld_json()
print_main_article_metadata()
print_references()
