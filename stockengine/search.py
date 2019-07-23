import json
import requests
from lxml import html

def search_stock(q):
    url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + q + "&apikey=76B2BGRH6OJS3Z0I"
    req = requests.get(url)
    res = json.loads(req.content)['bestMatches']

    return res[0]["1. symbol"]
    