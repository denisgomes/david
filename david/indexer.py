"""User site repository and search index.

Spiders crawl the web, extract text from urls and generate relevant keywords
based on different algorithms. For each url, the following items of data is
stored inside a sqlite repository i.e. database:

* the url,
* the title,
* the raw html,
* html hash,
* pagerank

The documents table is a fts3 table.

Sites
-----
id, hash, raw_html (compressed), weight (pagerank weight)

https://sqlite.org/fts3.html#matchinfo

Documents (FTS)
---------------
rowid, url, title, text

FTS is used along with ranking functions such as bm95 to get pages that match
terms most closely.

A vector of weights is dotted with the weights for those types to get a number
value of relevance. The relevance score is then multiplied by the pagerank to
calculate the final score.
"""

import hashlib
import sqlite3
from urllib.request import urlopen
import zlib

from lxml import html
from lxml.html.clean import Cleaner
import requests

from david.parser import HTMLTextParser


def md5sum(text):
    return hashlib.md5(text).hexdigest()


def zip(data):
    return zlib.compress(data, 9)


def unzip(data):
    return zlib.decompress(data)


def clean_html(url, blacklist):
    res = requests.get(url)
    doc = html.document_fromstring(res.content)

    cleaner = Cleaner(remove_tags=blacklist, style=True)
    d = cleaner.clean_html(doc)
    # print(d.text_content())

    # return set(d.text_content().split()) - stopwords
    return d.text_content()


class Indexer:
    """Manage a database of hypertext documents stored on disk."""

    database = "repository.db"

    def __init__(self):
        self.create_database(self.database)
        self.parser = HTMLTextParser()

    def create_database(self, name):
        """Create the document repository if one does not exist."""
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()

        # enable extension loading
        self.conn.enable_load_extension(True)

        # register sql functions
        self.conn.create_function("zip", 1, zip)
        self.conn.create_function("unzip", 2, unzip)

        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                hash TEXT,
                html BLOB,
                weight FLOAT,
                url,
                title,
                content
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts4 (
                content="sites",
                url,
                title,
                content,
                compress=zip,
                uncompress=unzip
            );
            """)

        self.conn.commit()
        # self.conn.close()

    def insert(self, url, doc):
        """Add an url and the corresponding document to the index."""
        print(url)

        text, urls = self.parser.parse(doc.decode("utf-8"))

        self.cur.execute("""
            INSERT INTO docs (
                url,
                title,
                content)
            VALUES (?, ?, ?)
            """, (url, "", doc)
            )

        self.conn.commit()

    def delete(self, url):
        pass

    def update(self, url):
        pass

    def search(self, query):
        """Do a full text search of the index and return a list of urls with
        the best rank based on the input query string.
        """
        raise NotImplementedError("implement")

    def rank(self):
        """Run the pagerank algorithm for the entire database."""
        raise NotImplementedError("implement")

    def close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    url = "https://www.msn.com/en-us/news/technology/amazon-wont-commit-to-jeff-bezos-testimony-over-misuse-of-seller-data/ar-BB14b9ZB"
    blacklist = ["noscript", "script", "[document]", "header", "html", "meta", "head", "input", "style"]

    # doc = urlopen(url, timeout=5).read()
    indexer = Indexer()
    # indexer.insert(url, doc)
