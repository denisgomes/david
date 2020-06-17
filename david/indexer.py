"""User site repository and search index.

Spiders crawl the web, extract text from urls and generate relevant keywords
based on different algorithms. For each url, the following items of data is
stored inside a sqlite repository i.e. database:

* the url,
* the title,
* h1,
* h2,
* h3,
* content,
* the raw html (compressed), <--- needed?
* html or content hash, <--- not sure which works best
* external urls (compressed, space separated),
* pagerank

The documents table is a fts4 table.

Sites
-----
id, hash, raw_html (compressed), weight (pagerank weight)

https://sqlite.org/fts3.html#matchinfo

Documents (FTS)
---------------
rowid, url, title, h1, h2, h3, content, raw html, external urls, pagerank

FTS is used along with ranking functions such as bm95 to get pages that match
terms most closely.

A vector of weights is dotted with the weights for those types to get a number
value of relevance. The relevance score is then multiplied by the pagerank to
calculate the final score.
"""

import logging
import sqlite3
import threading
from urllib.request import urlopen
import zlib

from lxml import html
from lxml.html.clean import Cleaner
import requests
# import sqlite_fts4


from david.conf import indexer_options as io
from david.parser import HTMLTextParser
from david.extern.sqlite_fts4 import sqlite_fts4


# report critial levels above 'warning', (i.e. 'error' and 'critical'),
# default
logging.basicConfig(level=logging.ERROR)


def zlibzip(data):
    return zlib.compress(data.encode("utf-8"), 9)


def zlibunzip(data):
    return zlib.decompress(data).decode("utf-8")


def clean_html(url, blacklist):
    res = requests.get(url)
    doc = html.document_fromstring(res.content)

    cleaner = Cleaner(remove_tags=blacklist, style=True)
    d = cleaner.clean_html(doc)
    # print(d.text_content())

    # return set(d.text_content().split()) - stopwords
    return d.text_content()


def make_repo(name):
    """Create the document repository if one does not exist."""
    conn = sqlite3.connect(name)
    curs = conn.cursor()

    # may need to be repeated everytime a connection is established

    # enable extension loading
    conn.enable_load_extension(True)

    # define pragmas as needed

    # register sql functions to use with fts4 tables
    conn.create_function("zlibzip", 1, zlibzip)
    conn.create_function("zlibunzip", 2, zlibunzip)

    curs.executescript("""
        CREATE TABLE IF NOT EXISTS sites (
            docid INTEGER PRIMARY KEY,
            url,
            title,
            h1,
            h2,
            h3,
            content,
            html TEXT,
            hash TEXT,
            weight FLOAT
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts4 (
            content="sites",
            url,
            title,
            h1,
            h2,
            h3,
            content,
            compress=zlibzip,
            uncompress=zlibunzip
        );

        CREATE TRIGGER sites_bu BEFORE UPDATE ON sites BEGIN
            DELETE FROM docs WHERE docid=old.rowid;
        END;
        CREATE TRIGGER sites_bd BEFORE DELETE ON sites BEGIN
            DELETE FROM docs WHERE docid=old.rowid;
        END;

        CREATE TRIGGER sites_au AFTER UPDATE ON sites BEGIN
            INSERT INTO docs(docid, url, title, h1, h2, h3, content)
            VALUES (new.rowid, new.url, new.title, new.h1, new.h2, new.h3,
                    new.content);
        END;
        CREATE TRIGGER sites_ai AFTER INSERT ON sites BEGIN
            INSERT INTO docs(docid, url, title, h1, h2, h3, content)
            VALUES (new.rowid, new.url, new.title, new.h1, new.h2, new.h3,
            new.content);
        END;
        """)

    conn.commit()
    conn.close()


class Indexer:
    """Index a repository of hypertext documents stored on disk.

    External content FT4 files.
    """

    debug = False

    def __init__(self):
        self.lock = threading.Lock()    # write lock

        # create database connect and cursor
        self.conn = sqlite3.connect(io["repository"], check_same_thread=False)
        self.curs = self.conn.cursor()

        # enable extension loading
        self.conn.enable_load_extension(True)

        # register sql functions to use with fts4 tables
        self.conn.create_function("zlibzip", 1, zlibzip)
        self.conn.create_function("zlibunzip", 1, zlibunzip)

        # register ranking functions
        sqlite_fts4.register_functions(self.conn)

        if self.debug:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)

    def insert(self, url, title, h1, h2, h3, content, html, hash):
        """Add an url and the corresponding document to the index.

        First check to see if the document has already been indexed by
        comparing the hash.
        """
        try:
            with self.lock:
                self.curs.execute("""
                INSERT INTO sites(url, title, h1, h2, h3, content, html, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (url, title, h1, h2, h3, content, zlibzip(html), hash)
                )
                self.conn.commit()
        except Exception:
            logging.exception("unable to insert url, %s" % url)

    def delete(self, url):
        pass

    def update(self, url):
        pass

    def search(self, query, limit=10, page=0):
        """Do a full text search of the index and return a list of urls with
        the best rank based on the input query string. Based on the sqlite3
        documentation query from, https://sqlite.org/fts3.html.
        """
        self.curs.execute("""
            SELECT url, title, snippet(docs, '**', '**', '...', 5, 25) FROM docs JOIN (
                SELECT docid, rank_bm25(matchinfo(docs, "pcnalx")) AS rank
                FROM docs JOIN sites USING(docid)
                WHERE docs MATCH ?
                ORDER BY rank DESC
                LIMIT ? OFFSET ?
            ) AS ranktable USING(docid)
            WHERE docs MATCH ?
            ORDER BY ranktable.rank DESC
            """, (query, limit, page, query)
            )

        return self.curs.fetchall()

    def pagerank(self):
        """Run the pagerank algorithm for the entire database."""
        raise NotImplementedError("implement")

    def close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    indexer = Indexer()
