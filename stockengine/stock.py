import requests
import selectolax.parser as sp

ALPHA_API_KEY = "76B2BGRH6OJS3Z0I"
NAME_FILTER = {
    ord(" "): "_",
    ord("."): "",
    ord("("): "",
    ord(")"): "",
    ord("'"): "",
}

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

    def profile(self):
        prof = dict()
        url = "https://finance.yahoo.com/quote/{}".format(self.symbol.upper())
        req = requests.get(url)
        res = req.content

        if req.status_code != 200:
            return {'error': 'Not Founded'}

        # Check if company exists
        exists_check = sp.HTMLParser(res).css("section span")
        if len(exists_check) >= 2 and exists_check[1].text() == "All (0)":
            return {'error': 'Not Founded'}

        # Extract h1 elements
        h1_raw = sp.HTMLParser(res).css("h1")
        company_title = h1_raw[0].text()
        prof["symbol"] = self.symbol
        prof["company_title"] = company_title[company_title.find('-')+2:]

        # Extract span elements
        span_raw = sp.HTMLParser(res).css("span")[13:]
        
        prof["exchange"] = span_raw[0].text()[0:span_raw[0].text().find('-')-1]
        prof["price"] = span_raw[1].text()
        prof["change_amount"] = span_raw[2].text()[0:span_raw[2].text().find(" ")]
        prof["change_percentage"] = span_raw[2].text()[span_raw[2].text().find("(")+1:span_raw[2].text().find("%")]
        
        for node in range(0, len(span_raw)):
            if span_raw[node].text() == "Previous Close":
                for ind in range(node, node + 22, 2):
                    key = span_raw[ind].text().lower().translate(NAME_FILTER)
                    val = span_raw[ind+1].text()
                    prof[key] = val
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
