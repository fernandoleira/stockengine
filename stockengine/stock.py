import requests
from lxml import html

ALPHA_API_KEY = "76B2BGRH6OJS3Z0I"

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def profile(self):
        prof = dict()
        url = "https://money.cnn.com/quote/quote.html?symb={}".format(self.symbol.upper())
        req = requests.get(url)
        res = html.fromstring(req.content)

        if req.status_code != 200:
            return {'error': 'Not Founded'}

        # Check if company exists
        if res.xpath("//h1//text()")[0] == "Symbol not found":
            return {"error": "stock not founded"}

        # Find company information
        prof["Symbol"] = self.symbol
        prof["Company Name"] = res.xpath('//h1[@class="wsod_fLeft"]//text()')[0][0:-1]
        prof["Price ($)"] = res.xpath('//td[@class="wsod_last"]//text()')[0]
        prof["Change ($)"] = res.xpath('//td[@class="wsod_change"]//text()')[1]
        prof["Change (%)"] = res.xpath('//td[@class="wsod_change"]//text()')[3][0:-1]
        prof["YTD"] = res.xpath('//td[@class="wsod_ytd"]//text()')[0][0:-1]

        raw_key = res.xpath('//div[@class="clearfix wsod_DataColumnLeft"]//text()')[1:]
        for i in range(0, len(raw_key), 2):
            prof[raw_key[i]] = raw_key[i+1]
            if raw_key[i] == 'Market cap':
                break

        return prof

    def intraday_time_series(self, interval="5min"):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + \
            self.symbol + "&interval=" + interval + "&apikey=" + ALPHA_API_KEY
        req = requests.get(url)
        res = eval(req.text)['Time Series (' + interval + ')']

        data = dict()
        for key, val in res.items():
            change_per = (float(val['4. close']) -
                          float(val['1. open']))/float(val['1. open'])

            data[key] = {
                "Open": float(val['1. open']),
                "High": float(val['2. high']),
                "Low": float(val['3. low']),
                "Close": float(val['4. close']),
                "Change Percentage": round(float(change_per), 3),
                "Volume": float(val['5. volume']),
            }

        return data

    def daily_time_series(self, amount="compact"):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=" + \
            amount + "&symbol=" + self.symbol + "&apikey=" + ALPHA_API_KEY
        req = requests.get(url)
        res = eval(req.text)['Time Series (Daily)']

        data = dict()
        for key, val in res.items():
            change_per = (float(val['4. close']) -
                          float(val['1. open']))/float(val['1. open'])

            data[key] = {
                "Open": float(val['1. open']),
                "High": float(val['2. high']),
                "Low": float(val['3. low']),
                "Close": float(val['4. close']),
                "Adjusted Close": float(val['5. adjusted close']),
                "Change Percentage": round(float(change_per), 3),
                "Volume": float(val['6. volume']),
                "Dividend": float(val['7. dividend amount']),
            }

        return data

    def monthly_time_series(self):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + \
            self.symbol + "&apikey=" + ALPHA_API_KEY
        req = requests.get(url)
        res = eval(req.text)['Monthly Adjusted Time Series']

        data = dict()
        for key, val in res.items():
            change_per = (float(val['4. close']) -
                          float(val['1. open']))/float(val['1. open'])

            data[key] = {
                "Open": float(val['1. open']),
                "High": float(val['2. high']),
                "Low": float(val['3. low']),
                "Close": float(val['4. close']),
                "Adjusted Close": float(val['5. adjusted close']),
                "Change Percentage": round(float(change_per), 3),
                "Volume": float(val['6. volume']),
                "Dividend": float(val['7. dividend amount']),
            }

        return data
