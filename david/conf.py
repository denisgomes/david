"""dAvId system settings and configurations"""

import os


# project root
project_root = os.path.abspath(os.path.dirname(__name__))

# repository
repository = "test.repo"


crawler_options = {
    "debug": False,         # crawl in debug mode
    "level": 100,           # total levels to jump
    "max": 1000,            # max number of urls per level
    "total": 5000,          # minimum number of urls to crawl
    "follow": True,         # follow external urls
    "respect": True,        # respect host servers
    "robots": True,         # read robots file
    "timeout": 3,           # request connection timeout
    "wait": [1, 3],         # wait time range
    "history": 2000,        # visit history deque size
}


indexer_options = {
    "debug": False,         # index in debug mode
    "repository": os.path.join(project_root, repository),
}


# weights applied to rank function of FTS table
# all the weights should add up to a total of 1
weights = [
        1.25,               # column 1, url
        1.25,               # column 2, title
        1.10,               # column 3, h1
        1.05,               # column 4, h2
        1.05,               # column 5, h3
        1.30                # column 6, content
]
