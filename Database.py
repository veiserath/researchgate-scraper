import psycopg2
import requests
from bs4 import BeautifulSoup
from lxml import etree

import paths


def connect_to_database():
    con = psycopg2.connect(database=paths.DATABASE, user=paths.USER,
                           password=paths.PASSWORD, host=paths.HOST,
                           port=paths.PORT)
    print("Database opened successfully")
    return con


con = connect_to_database()


def create_tables():
    try:
        with con.cursor() as cursor:
            cursor.execute(open("Database_Model.sql", "r").read())
            con.commit()
            print("Created database")
    except psycopg2.errors.DuplicateTable:
        print("Tables already created!")



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
    except psycopg2.errors.InFailedSqlTransaction:
        print("Article was already added!")

def insert_reference_to_database(title, url, date, publisher, main_article_url, reference_url):
    cur = con.cursor()
    insert_article_to_database(title, url, date, publisher)
    try:
        cur.execute(
            "INSERT INTO ARTICLEREFERENCE (main_article_url,reference_article_url) "
            "VALUES (%(main_article_url)s,%(reference_url)s)",
            {'main_article_url': main_article_url, 'reference_url': reference_url})
    except psycopg2.errors.InFailedSqlTransaction:
        print("Reference was already added!")

def insert_references_to_database(article):
    for item in article.references:
        insert_reference_to_database(item["title"], item["url"], item["date"], item["publisher"], article.url,
                                     item["url"])


def insert_citation_to_database(article_url_to_insert, citation_url_to_insert):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO ARTICLECITATION (article_id,citation_id) VALUES (article_id_to_insert,citation_id_to_insert)")


def get_elements_from_database():
    cur = con.cursor()
    cur.execute("SELECT * FROM ARTICLE WHERE citation_count IS NULL")
    for element in cur.fetchall():
        URL = element[1]
        REQUEST = requests.get(URL)
        PARSER = "html.parser"
        SOUP = BeautifulSoup(REQUEST.text, PARSER)
        DOM = etree.HTML(str(SOUP))


# create_database()
# insert_article_to_database('title_function', 'url_from_hell', '2006-01-01', 'kacprowski', 10, 200)


def close_connection():
    con.close()
