import time
from bs4 import BeautifulSoup
import requests
import json
from lxml import etree

url = "https://www.researchgate.net/publication/220591356_Identifying_Software_Project_Risks_An_International_Delphi_Study"
request = requests.get(url)
parser = "html.parser"
soup = BeautifulSoup(request.text, parser)
dom = etree.HTML(str(soup))


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
    citation = str(dom.xpath("//div[contains(text(),'Citations')]/text()")[0])
    return get_count(citation)


def get_references_count():
    references = str(dom.xpath("//div[contains(text(),'References')]/text()")[0])
    return get_count(references)


def get_ld_json() -> dict:
    return json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))


def export_to_pdf():
    paper_info = {
        'title': result["headline"],
        'url': result["mainEntityOfPage"],
        'date': result["datePublished"],
        'publisher': result["publisher"]["name"],
        'citation count': get_citation_count(),
        'reference count': get_references_count(),
        'references': get_references(),
        'citations': get_citations()
    }
    result_json = json.dumps(paper_info)

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





get_citation_count()
result = get_ld_json()



citations_range = len(result["citation"]) - 1 - len(get_citation_count())
# print_main_article_metadata()
# print_references()
export_to_pdf()
print(generate_tree_schema())