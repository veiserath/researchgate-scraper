import Database
import PdfExport
import Crawler

# Database.create_tables()


# article = Crawler.crawl_url("https://www.researchgate.net/publication/308413321_Knowledge_Gained_from_Twitter_Data")
#
# PdfExport.export_to_pdf(article=article)
#
# Database.insert_article_to_database(title=article.title, url=article.url, date=article.date,
#                                     publisher=article.publisher, citation_count=article.citation_count,
#                                     reference_count=article.reference_count)
#
# Database.insert_references_to_database(article=article)

null_elements = Database.get_elements_from_database()

print(null_elements)

for element in null_elements:
    try:
        article = Crawler.crawl_url(element[1])
        Database.update_article_in_database(article)
    except IndexError:
        print(element[1])

# article = Crawler.crawl_url("https://www.researchgate.net/publication/313559770_Nonparametric_Statistics_for_the_Behavioral_Sciences_ed_2")
# Database.update_article_in_database(article=article)

Database.close_connection()
