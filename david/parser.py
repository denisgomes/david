"""A simple HTML parser"""


from html.parser import HTMLParser
from urllib.request import urlopen


class HTMLTextParser(HTMLParser):

    _exclude_tags = ["script", "noscript", "head", "html", "header", "meta",
                     "input", "style"]

    _extract_tag_data = True

    _text = []

    _urls = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self._urls.add(value)

        self._extract_tag_data = True
        if tag in self._exclude_tags:
            self._extract_tag_data = False

    def handle_data(self, data):
        if self._extract_tag_data:
            data = data.split()     # remove newlines, etc

            if data:
                self._text.append(" ".join(data))
            else:
                self._text.append("\n")

    def handle_comment(self, comment):
        self._extract_tag_data = False

    def parse(self, html):
        self._text.clear()
        self._urls.clear()
        self.feed(str(html))

        return "".join(self._text[:]), self._urls.copy()


if __name__ == "__main__":
    html = urlopen("https://news.yahoo.com/").read()
    parser = HTMLTextParser()
    text, urls = parser.parse(html.decode("utf-8"))

    # print(text)
    print(urls)
