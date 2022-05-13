import requests
import re
import logging

class TelegramAPI:
    def __init__(self, token) -> None:
        self.token = token

    def sanitize(self, text):
        return re.sub(r"([_*~`>\#\+\-=|\.!])", r"\\\1", text)
    
    def api(self, method, params):
        url = "https://api.telegram.org/bot{}/{}".format(self.token, method)
        r = requests.post(url, params)
        if not r.json()['ok']:
            logging.error("Request failed")
        return r
            

    # send a simple text message
    def sendMessage(self, chat_id, text):
        params = {
            "chat_id": chat_id,
            "text": text
        }
        return self.api("sendMessage", params) 

    def sendArticle(self, chat_id, article):
        # tags = " ".join(["\#" + tag for tag in article.tags])
        text = "{}: {}\n{}".format(article['source'], article['title'], article['url'])
        params = {
            "chat_id": chat_id,
            "text": self.sanitize(text),
            "parse_mode": "MarkdownV2"
        }
        return self.api("sendMessage", params)
        
    def sendBatch(self, chat_id, articles):
        text = ""
        for article in articles:
            text += "{}: [{}]({})\n".format(article['source'], article['title'], article['url'])
        params = {
            "chat_id": chat_id,
            "text": self.sanitize(text),
            "parse_mode": "MarkdownV2"
        }
        return self.api("sendMessage", params)

    