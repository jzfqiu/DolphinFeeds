import requests

class TelegramAPI:
    def __init__(self, token) -> None:
        self.token = token
    
    def api(self, method, params):
        url = "https://api.telegram.org/bot{}/{}".format(self.token, method)
        r = requests.post(url, params)
        return r

    # send a simple text message
    def sendMessage(self, chat_id, text):
        params = {
            "chat_id": chat_id,
            "text": text
        }
        # TODO: response error handling
        return self.api("sendMessage", params)

    def sendArticle(self, chat_id, article):
        tags = " ".join(["\#" + tag for tag in article.tags])
        link = "[{}]({})".format(article.title, article.url)
        text = "{}: {}\n\n{}".format(article.source, link, tags)
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "MarkdownV2"
        }
        return self.api("sendMessage", params)
        
class TaggingAPI:
    def __init__(self, token) -> None:
        self.token = token

    