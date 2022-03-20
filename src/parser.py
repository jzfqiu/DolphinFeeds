from bs4 import BeautifulSoup
from datetime import datetime


class Parser:
    def __init__(self, source, tags):
        self.source = source
        self.tags = tags

    def parse(self, text):
        if self.source == "Lawfare":
            return self.parser_lawfare(text)

    def parser_lawfare(self, text):
        ret = []
        soup = BeautifulSoup(text, 'lxml')
        channel = soup.channel
        items = channel.find_all("item")
        for item in items:
            article = {}
            article["title"] = item.title.contents[0].strip()
            article["url"] = str(item).split("<link/>")[-1].split("\n")[0]
            article["pub_date"] = datetime.strptime(item.pubdate.contents[0], "%a, %d %b %Y %H:%M:%S %z")
            article["author"] = item.find("dc:creator").contents[0]
            # article["guid"] = item.guid.contents[0]
            # article["full_text"] = BeautifulSoup(item.description.contents[0]).text
            article["source"] = self.source
            article["tags"] = article.get("tags", []) + self.tags
            ret.append(article)
        return ret

        
