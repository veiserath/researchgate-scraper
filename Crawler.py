import json
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import etree

import paths
from Article import Article

URL = paths.URL
DOM = None


def crawl_url(url=paths.URL):
    global URL
    URL = url
    result = get_ld_json()
    # print_main_article_metadata(result)
    article = construct_article_object(result)
    return article


def get_ld_json() -> dict:
    REQUEST = requests.get(URL)
    PARSER = "html.parser"
    SOUP = BeautifulSoup(REQUEST.text, PARSER)
    global DOM
    DOM = etree.HTML(str(SOUP))
    return json.loads("".join(SOUP.find("script", {"type": "application/ld+json"}).contents))


def get_references(result, citations_range):
    references = []
    for i, item in enumerate(result["citation"]):
        if i >= citations_range:
            break
        paper_info = {
            'title': item["headline"],
            'url': item["mainEntityOfPage"],
            'date': item["datePublished"],
            'publisher': item["publisher"]["name"],
        }
        references.append(paper_info)
    return references


def get_citations(result, citations_range):
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


def get_count(string):
    count = ""
    for item in string:
        if item.isdigit():
            count += item
    return count


def get_citation_count():
    try:
        citation = str(DOM.xpath("//div[contains(text(),'Citations')]/text()")[0])
    except IndexError:
        return 0
    return int(get_count(citation))


def get_references_count():
    try:
        references = str(DOM.xpath("//div[contains(text(),'References')]/text()")[0])
    except IndexError:
        return 0
    return int(get_count(references))


def print_main_article_metadata(result):
    print(result["headline"])
    print(result["datePublished"])
    print(result["mainEntityOfPage"])
    # make it a one-liner
    for item in result["author"]:
        print(item["name"])
    print(result["publisher"]["name"])
    print("====")
    print("citation " + str(get_citation_count()))
    print("references " + str(get_references_count()))


def print_references(result):
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


def construct_article_object(result):
    citations_range = abs(len(result["citation"]) - 1 - get_citation_count())
    title = result["headline"]
    url = result["mainEntityOfPage"]
    date = result["datePublished"]
    publisher = result["publisher"]["name"]

    citation_count = int(get_citation_count())
    reference_count = int(get_references_count())
    references = get_references(result, citations_range)
    citations = get_citations(result, citations_range)
    article = Article(title=title, url=url, date=date, publisher=publisher, citation_count=citation_count,
                      reference_count=reference_count, references=references, citations=citations)
    print(article.title)
    return article
