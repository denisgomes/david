"""Implementation of a web spider"""

from arackpy import spider

import lxml


class Crawler(spider.Spider):

    thread_safe_parse = True    # enforce sqlite db write is threadsafe

    def parse(self, url, html):
        print(url)


def start_crawler(args):
    """args is the namespace of command line arguments supplied by the
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
