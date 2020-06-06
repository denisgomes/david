"""The dAvId Command Line Interface (CLI).

$ david startserver
$ david stopserver

$ david crawl url1, url2, ...
$ david crawl -p 123.123.123.123 -L 100 -T 1000 url1, url2, ..., urlN
"""

import argparse

from conf import crawler_options as co
from crawler import start_crawler


# top level parsers
parser = argparse.ArgumentParser(prog="dAvId")
parser.add_argument("--version", action="version", version="%(prog)s 0.1",
                    help="program version information")

# crawl subparser
crawl_subparser = parser.add_subparsers(title="crawl",
                                        description="crawl and index",
                                        help="crawling subcommands",
                                        dest="name"     # handle to subparser
                                        )
crawl = crawl_subparser.add_parser("crawl", help="list of urls to crawl")
crawl.add_argument("start_urls", nargs="+",     # at least one pos arg required
                   help="list of start urls")
crawl.add_argument("-p", "--proxy", dest="proxy", nargs="+",
                   help="list of proxies to use")
crawl.add_argument("-m", "--max", dest="max", type=int, default=co["max"],
                   help="max number of urls per level")
crawl.add_argument("-L", "--level", dest="level", type=int,
                   default=co["level"], help="total number of levels to jump")
crawl.add_argument("-T", "--total", dest="total", type=int,
                   default=co["total"], help="total number of urls to crawl")
crawl.add_argument("-D", "--debug", dest="debug", type=bool,
                   default=co["debug"], help="crawl using debug mode")
crawl.add_argument("-f", "--follow", dest="follow", type=bool,
                   default=co["follow"], help="follow external links")
crawl.add_argument("-r", "--robots", dest="robots", type=bool,
                   default=co["robots"], help="honor robots.txt files")
crawl.add_argument("-R", "--respect", dest="respect", type=bool,
                   default=co["respect"],
                   help="respect host by adhering to a wait time")
crawl.add_argument("-t", "--timeout", dest="timeout", type=int,
                   default=co["timeout"], help="request connection timeout")
crawl.add_argument("-w", "--wait", dest="wait", type=int,
                   default=co["wait"], nargs=2, help="respect wait time range")
crawl.add_argument("-H", "--history", dest="history", type=int,
                   default=co["history"], help="visit history deque size")

# index subparser
# ...

if __name__ == "__main__":
    args = parser.parse_args()

    if args.name == "crawl":
        start_crawler(args)
