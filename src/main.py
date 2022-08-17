import datetime

import feedparser
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


def update_db(url: str, tags, source, db: Database):
    data = feedparser.parse(url)
    updated = 0
    for entry in data.entries:
        article = {
            "id": hash_md5(entry.link),
            "title": entry.title,
            "url": entry.link,
            "pub_date": entry.get("published_parsed", datetime.datetime.now()),
            "tags": tags,
            "source": source,
        }
        # compare feed with existing in db
        if len(db.filter("Articles", {"id": article['id']})) > 0:
            pass
        else:
            # send update to database
            article['sent'] = 0
            db.insert_one("Articles", article)
            updated += 1

    logging.info(f"{d['source']} updated with {updated} new articles")



if __name__ == "__main__":
    db = Database(RDS_ENDPOINT, RDS_USER, RDS_PWD, RDS_DATABASE)
    updated = 0
    
    for d in SOURCES:
        updated = update_db(d["url"], d["tags"], d["source"], db)

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
            res = telegramBot.sendBatch(TELEGRAM_FEED_CHANNEL_ID, articles[i:i+BATCH_SIZE+5])
            i += BATCH_SIZE+5
    
    db.close()
        