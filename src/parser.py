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
        channel = soup.channel
        try:
            items = channel.find_all("item")
        except AttributeError as e:
            logging.error("No item found in soup")
            return []
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
                raise
        return ret

    def parse_title(self, item):
        dom = item.title
        if dom.contents:
            return self.strip_cdata(dom.contents[0].strip())
        else:
            logging.error("No title information in " + str(item))
            raise Exception
    
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
        dom = item.pubdate
        if not dom:
            # no pubdate attribute
            return datetime.now()
        content = dom.contents[0]
        if content[-1].isalpha():
            # timezone is spelled out in letters (e.g. UTC instead of +0000)
            # US timezone conversion: https://www.timetemperature.com/abbreviations/united_states_time_zone_abbreviations.shtml 
            tokens = content.split()
            timezone = tokens.pop(-1)
            tokens.append(timezone_table[timezone])
            content = " ".join(tokens)
        return datetime.strptime(content, "%a, %d %b %Y %H:%M:%S %z")


    def parse_author(self, item):
        dom = item.find("dc:creator")
        if not dom:
            # <author>noreply@blogger.com (Ravie Lakshmanan)</author>
            dom = item.find('author')
            if not dom: 
                return ""
            tokens = re.split('[\(\)]', dom.contents[0])
            return tokens[1]
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

