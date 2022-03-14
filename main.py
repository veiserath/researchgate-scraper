import json
from bs4 import BeautifulSoup
import requests


url = "https://www.researchgate.net/publication/324010445_Changing_the_Model_of_Maritime_Navigation"


def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    # return json.loads("".join(soup.find('script', {'type': 'application/ld+json'})))
    p = str(soup.find('script', {'type': 'application/ld+json'}))
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

def print_main_article_metadata(json):
    print(result["headline"])
    print(result["datePublished"])
    print(result["mainEntityOfPage"])
    # make it a one-liner
    for item in result["author"]:
        print(item["name"])
    print(result["publisher"]["name"])
    print("====")

result = get_ld_json(url)
print_main_article_metadata(json)



for item in result["citation"]:
    print(item["headline"])
    print(item["datePublished"])
    print(item["mainEntityOfPage"])
    # make it a one-liner
    for subitem in item["author"]:
        print(subitem["name"])
    print(item["publisher"]["name"])
    print("===")