"""Implementation of a web spider.


The spider is responsible for inserting items into the repository.

"""

import hashlib

from arackpy import spider

from david.parser import HTMLTextParser
from david.indexer import Indexer


def md5sum(text):
    return hashlib.md5(text).hexdigest()


def start_crawler(args):
    """Run a crawler.

        args is the namespace of command line arguments supplied by the
        crawl subparser.
    """
    # set top level crawl options
    Crawler.start_urls = args.start_urls
    Crawler.follow_external_links = args.follow
    Crawler.visit_history_limit = args.history
    Crawler.respect_server = args.respect
    Crawler.read_robots_file = args.robots
    Crawler.wait_time_range = args.wait
    Crawler.timeout = args.timeout
    Crawler.max_urls_per_level = args.max
    Crawler.max_level = args.level
    Crawler.max_urls = args.total
    Crawler.debug = args.debug

    # if using proxies, initialize proxyspider
    if args.proxy:
        crawler = Crawler(backend="proxy", proxies=args.proxy)
    else:
        crawler = Crawler()     # default backend

    # run
    crawler.crawl()


class Crawler(spider.Spider):
    # options
    thread_safe_parse = False   # safety up to indexer

    def __init__(self, backend="default", **kwargs):
        self.indexer = Indexer()    # shared across threads
        super(Crawler, self).__init__(backend=backend, **kwargs)

    def parse(self, url, html):
        # multithreaded parsing and execution
        parser = HTMLTextParser()

        try:
            data = parser.parse(html)

            title = "".join(data["title"])
            print(title)

            # similar heading joined
            h1 = " ".join(data["h1"])
            h2 = " ".join(data["h2"])
            h3 = " ".join(data["h3"])

            # text content
            content = " ".join(data["content"])
            # print(content)
            hash = md5sum(content.encode("utf-8"))

            self.indexer.insert(url, title, h1, h2, h3, content, html, hash)

        except Exception as e:
            print(e)
