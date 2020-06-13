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
    "total": 5000,          # total number of urls to crawl
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
