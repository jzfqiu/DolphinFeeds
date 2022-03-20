from hashlib import md5
from config import TEXTRAZOR_TOKEN
import textrazor

def hash_md5(s):
    h = md5()
    h.update(s.encode("utf-8"))
    return h.hexdigest()[:10]

class Article:
    """Representation of an article, initiated by a dict

    Attribute: 
    """
    def __init__(self, data) -> None:
        self.id = ""
        self.title = data["title"]
        self.url = data["url"]
        self.pub_date = data["pub_date"]
        self.author = data["author"]
        self.source = data["source"]
        self.tags = data["tags"]
        
        if not self.id:
            # need to create id
            self.id = hash_md5(data["title"])
    
    def getTags(self):
        # textrazor.api_key = TEXTRAZOR_TOKEN
        # client = textrazor.TextRazor(extractors=["entities", "topics"])
        # response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")
        # for entity in response.entities():
        #     print(entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)
        pass

    def getSummary(self):
        pass
    