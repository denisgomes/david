"""A simple HTML parser"""


from html.parser import HTMLParser
from urllib.request import urlopen

from collections import defaultdict


class HTMLTextParser(HTMLParser):
    """Custom html parser"""

    exclude_tags = ["script", "noscript", "head", "html", "header", "meta",
                    "input", "style"]
    extract_tag_data = True
    tag = None
    data = defaultdict(list)

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        # if tag == "a":
        #     for attr, value in attrs:
        #         if attr == "href":
        #             self.data["urls"].append(value)

        self.extract_tag_data = True
        if tag in self.exclude_tags:
            self.extract_tag_data = False

    def handle_data(self, data):
        if self.extract_tag_data:
            data = data.splitlines()    # remove newlines, etc

            if self.tag == "title":
                self.data["title"].extend(data)

            elif self.tag == "h1":
                self.data["h1"].extend(data)

            elif self.tag == "h2":
                self.data["h2"].extend(data)

            elif self.tag == "h3":
                self.data["h3"].extend(data)

            else:
                self.data["content"].extend(data)

    def handle_comment(self, comment):
        self.extract_tag_data = False

    def parse(self, html):
        self.feed(str(html))

        data = self.data.copy()
        self.data.clear()

        return data


if __name__ == "__main__":
    from gensim.summarization import summarize

    html = urlopen("https://news.yahoo.com/republican-senators-respond-disbelief-trump-082644931.html").read()
    parser = HTMLTextParser()

    data = parser.parse(html.decode("utf-8"))
    # print(" ".join(data["content"]))

    # text = " ".join(data["content"])
    print(data["h1"])
    # print(summarize(text))
