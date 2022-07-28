import logging
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
        if soup.find("channel"):
            feed = soup.channel
            items = feed.find_all("item")
        elif soup.find("feed"):
            feed = soup.feed
            items = feed.find_all("entry")
        for item in items:
            article = {}
            try:
                article["title"] = self.parse_title(item)
                article["url"] = self.parse_url(item)
                article["pub_date"] = self.parse_pubdate(item)
                article["author"] = self.parse_author(item)
                article["source"] = self.source
                article["tags"] = article.get("tags", []) + self.tags
                ret.append(article)
            except:
                logging.error(item)
                # raise
        return ret

    def parse_title(self, item):
        dom = item.title
        if dom.contents:
            return self.strip_cdata(dom.contents[0].strip())
        else:
            logging.error("No title information in " + str(item))
            # raise Exception
    
    def parse_url(self, item):
        # <link/>url.com\n
        # <link/>url.com<author>
        url = re.split("[\n<]", str(item).split("<link/>")[-1])[0]
        if not url:
            # RAND specifics
            return item.id.text
        return url
        
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
        if item.pubdate:
            dom = item.pubdate
            content = dom.contents[0]
            if content[-1].isalpha():
                # timezone is spelled out in letters (e.g. UTC instead of +0000)
                # US timezone conversion: https://www.timetemperature.com/abbreviations/united_states_time_zone_abbreviations.shtml 
                tokens = content.split()
                timezone = tokens.pop(-1)
                tokens.append(timezone_table[timezone])
                content = " ".join(tokens)
            return datetime.strptime(content, "%a, %d %b %Y %H:%M:%S %z")
        elif item.published:
            # 2022-04-29T08:00:00Z
            dom = item.published
            return datetime.fromisoformat(dom.text[:-1])
        elif item.find("dc:date"):
            # <dc:date>2022-05-12T10:00:00+00:00</dc:date>
            dom = item.find("dc:date")
            return datetime.fromisoformat(dom.text)
        else:
            # no pubdate attribute
            return datetime.now()



    def parse_author(self, item):
        dom = item.find("dc:creator")
        if not dom:
            # <author>noreply@blogger.com (Ravie Lakshmanan)</author>
            dom = item.find('author')
            if not dom: 
                return ""
            # tokens = re.split('[\(\)]', dom.contents[0])
            ret = dom.text.strip()
            return ret
        if dom.contents:
            return self.strip_cdata(dom.contents[0])
        else:
            logging.error("No author information")
            return "Unknown"

    def strip_cdata(self, data):
        if "CDATA" in data:
            return re.split('[\[\]]', data)[2]
        else:
            return data

