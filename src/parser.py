from bs4 import BeautifulSoup
from datetime import datetime
import re


class Parser:
    def __init__(self, source, tags):
        self.source = source
        self.tags = tags

    def parse(self, text):
        ret = []
        soup = BeautifulSoup(text, 'lxml')
        channel = soup.channel
        items = channel.find_all("item")
        for item in items:
            article = {}
            article["title"] = self.parse_title(item)
            article["url"] = self.parse_url(item)
            article["pub_date"] = self.parse_pubdate(item)
            article["author"] = self.parse_author(item)
            article["source"] = self.source
            article["tags"] = article.get("tags", []) + self.tags
            ret.append(article)
        return ret

    def parse_title(self, item):
        dom = item.title.contents[0]
        return dom.strip()
    
    def parse_url(self, item):
        # <link/>url.com\n
        # <link/>url.com<author>
        tokens = re.split("[\n<]", str(item).split("<link/>")[-1])
        return tokens[0]
        
    def parse_pubdate(self, item):
        timezone_table = {
            "PST": "-0800",
            "PDT": "-0700",
            "MST": "-0700",
            "MDT": "-0600",
            "CST": "-0600",
            "CDT": "-0500",
            "EST": "-0500",
            "EDT": "-0400",
        }
        dom = item.pubdate.contents[0]
        if dom[-1].isalpha():
            # timezone is spelled out in letters (e.g. UTC instead of +0000)
            # US timezone conversion: https://www.timetemperature.com/abbreviations/united_states_time_zone_abbreviations.shtml 
            tokens = dom.split()
            timezone = tokens.pop(-1)
            tokens.append(timezone_table[timezone])
            dom = " ".join(tokens)
        return datetime.strptime(dom, "%a, %d %b %Y %H:%M:%S %z")


    def parse_author(self, item):
        dom = item.find("dc:creator")
        if not dom:
            # <author>noreply@blogger.com (Ravie Lakshmanan)</author>
            dom = item.find('author')
            tokens = re.split('[\(\)]', dom.contents[0])
            return tokens[1]
        tokens = re.split('[\[\]]', dom.contents[0])
        if len(tokens) > 2:
            return tokens[2]
        else:
            return dom.contents[0]

