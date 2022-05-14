from typing import List
import requests
from parser import Parser
from db import Database
from config import *
from api import TelegramAPI
from config import SOURCES, SLEEP_TIME
from hashlib import md5
import logging


"""
Set logging level: 
    logging.DEBUG:  print debug, info, warning, and error
    logging.INFO:   print info, warning, and error
    logging.WARNING: print warning and error only <- use this for release
"""
logging.basicConfig(
    format="[%(levelname)s] %(module)s:%(funcName)s:%(lineno)d - %(message)s",
    level=logging.INFO
)

def hash_md5(s):
    h = md5()
    h.update(s.encode("utf-8"))
    return h.hexdigest()[:10]


def update_db(url: str, source: str, tags: List[str], db):
    logging.info(f"Updating {source}...")
    # pull the latest feed
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}   
    r = requests.get(url, headers=headers)

    # parse feed 
    parser = Parser(source, tags)
    articles = parser.parse(r.text)

    # initialize services
    if not db:
        return 0
    
    updated = 0

    for article in articles:
        article['id'] = hash_md5(article["url"])
        # compare feed with existing in db 
        if len(db.filter("Articles", {"id": article['id']})) > 0:
            pass
        else:
            # send update to database 
            article['sent'] = 0
            db.insert_one("Articles", article)
            updated += 1
    
    logging.info(f"{d['source']} updated with {updated} new articles")
    return updated



if __name__ == "__main__":
    db = Database(RDS_ENDPOINT, RDS_USER, RDS_PWD, RDS_DATABASE)
    updated = 0
    
    for d in SOURCES:
        updated = update_db(d["url"], d["source"], d["tags"], db)

    telegramBot = TelegramAPI(TELEGRAM_BOT_TOKEN)
    rows = db.filter("Articles", {"sent": 0})
    column_names = db.cursor.column_names
    if len(rows) >= BATCH_SIZE:
        articles = []
        for row in rows:
            article = {k: v for k, v in zip(column_names, row)}
            articles.append(article)
            db.update_by_id("Articles", article["id"], {"sent": 1})
    i = 0
    while i < len(articles):
        res = telegramBot.sendBatch(TELEGRAM_FEED_CHANNEL_ID, articles[i:i+BATCH_SIZE])
        i += BATCH_SIZE
    
    db.close()
        