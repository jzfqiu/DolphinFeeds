from hashlib import md5
import requests
from config import TEXTRAZOR_TOKEN, SMMRY_TOKEN
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
        textrazor.api_key = TEXTRAZOR_TOKEN
        client = textrazor.TextRazor(extractors=["topics"])
        response = client.analyze_url(self.url)
        print(self.url)
        for topic in response.topics():
            if topic.score > 0.7:
                print(topic.label, topic.score)
            # self.tags.append(topic.label)
            

    def getSummary(self):
        # A limit of 100 free API requests can be made daily, 
        # and each request must be at least 10 seconds apart.
        url = "https://api.smmry.com"
        params = {
            "SM_API_KEY": SMMRY_TOKEN,
            "SM_URL": self.url,
        }
        r = requests.post(url, params=params)
        response = r.json()
        self.summary = response['sm_api_content']


        

    