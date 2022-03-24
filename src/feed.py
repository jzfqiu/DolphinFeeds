from typing import List
import requests
from parser import Parser
from db import Database
from article import Article
from config import *
from api import TelegramAPI


class Feed:
    """Representation of a single RSS feed

    Attributes:
        name: name of the rss
        url: url of the rss
        tags: tags associated with the rss
    """
    def __init__(self, url: str, source: str, tags: List[str]) -> None:
        self.url = url
        self.source = source
        self.tags = tags

    

    def update(self):
        # pull the latest feed,     
        r = requests.get(self.url)

        # parse feed 
        parser = Parser(self.source, self.tags)
        try:
            articles_data = parser.parse(r.text)
        except:
            print(r.text)
            raise

        # initiaize services
        db = Database(RDS_ENDPOINT, RDS_USER, RDS_PASSWORD, RDS_DATABASE)
        telegramBot = TelegramAPI(TELEGRAM_BOT_TOKEN)
        
        updated = 0

        for article_data in articles_data:
            article = Article(article_data)
            
            # compare feed with existing in db 
            if len(db.filter("Articles", {"id": article.id})) > 0:
                pass
            
            else:
                # TODO: filter tags
                # article.getTags()

                # TODO: use inline keyboard to generate summary
                # article.getSummary()

                # send update to telegram
                telegramBot.sendArticle(TELEGRAM_FEED_CHANNEL_ID, article)
                
                # send update to database 
                db.insert("Articles", [article.__dict__])
                
                updated += 1
        
        db.close()
        return updated

