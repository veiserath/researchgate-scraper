import json

import Crawler


def export_to_pdf(article):
    paper_info = {
        'title': article.title,
        'url': article.url,
        'date': article.date,
        'publisher': article.publisher,
        'citation count': article.citation_count,
        'reference count': article.reference_count,
        'references': article.references,
        'citations': article.citations
    }
    result_json = json.dumps(paper_info)
    with open("result.json", "w") as outfile:
        outfile.write(result_json)
