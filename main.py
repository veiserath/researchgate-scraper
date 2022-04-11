import ResultsExport
import Crawler
import Database

# Database.create_tables()


# article = Crawler.crawl_url(
#     "https://www.researchgate.net/publication/328362505_Deep_Confidence_A_Computationally_Efficient_Framework_for_Calculating_Reliable_Prediction_Errors_for_Deep_Neural_Networks")
#
# ResultsExport.export_to_json(article=article)
#
# Database.insert_article_to_database(title=article.title, url=article.url, date=article.date,
#                                     publisher=article.publisher, citation_count=article.citation_count,
#                                     reference_count=article.reference_count)
#
# Database.insert_references_to_database(article=article)
# Database.insert_citations_to_database(article=article)
#
# null_elements = Database.get_elements_from_database_with_null_citations()
#
# print(len(null_elements))
# for element in null_elements:
#     article = Crawler.crawl_url(element[1])
#     Database.update_article_in_database(article)
#     Database.insert_references_to_database(article=article)
#     Database.insert_citations_to_database(article=article)
#
# Database.close_connection()


ResultsExport.export_to_javascript()
