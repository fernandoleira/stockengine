from datetime import datetime, timedelta
import requests
from lxml import html
from stockengine.stock import Stock

class Dividend:
    def __init__(self, date):
        self.date = date

    def dividend_list(self):
        url = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=" + self.date
        req = requests.get(url)
        res = html.fromstring(req.content)
        
        raw_stocks = list()
        table_rows = res.xpath('//table[@id="Table1"]//tr')
        for row in table_rows:
            cols = list(row.xpath('.//td//text()'))
            raw_stocks.append(cols)

        stocks = list()
        for raw in raw_stocks[1:]:
            name = raw[0]
            symbol = name[name.find('(')+1:name.find(')')].upper()
            price = Stock(symbol).profile()["Price ($)"]
            if price == 'n/a':
                yield_div = 'n/a'
            else:
                yield_div = round(float(raw[2])/float(price), 3)
            
            stocks.append({"Symbol": symbol, "Name": name[0:name.find('(')-1], "Dividend": float(raw[2]), "Price": price, "Yield": yield_div})

        return stocks

    def today_dividends():
        day_name = datetime.now()
        if day_name.strftime("%A") == "Friday":
            day_name += timedelta(days=3)
        elif day_name.strftime("%A") == "Saturday":
            day_name += timedelta(days=2)
        else:
            day_name += timedelta(days=1)

        return self.dividend_list()


"""

divs = Dividend(day_name.strftime("%Y-%m-%d")).dividend_list()
tops = []

for t in range(3):
    max_div = 0
    max_stock = dict()
    for stock in divs:
        if stock["Yield"] > max_div and stock not in tops:
            max_div = stock["Yield"]
            max_stock = stock

    tops.append(max_stock)

print(tops)"""