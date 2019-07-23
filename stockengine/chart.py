import datetime
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib
import matplotlib.pyplot as plt
from stockengine.stock import Stock

PLT_STYLE = "ggplot"
VALID_GROUPS = ["open", "close", "change", "volume"]
VALID_BLOCKS = ["intraday", "daily", "monthly"]


def generate_chart(symbol, key_group, block):
    # Pandas Config
    register_matplotlib_converters()
    plt.style.use(PLT_STYLE)

    stock = Stock(symbol)

    # Check Block
    if block == "intraday":
        interval = stock.intraday_time_series()
    elif block == "daily":
        interval = stock.daily_time_series()
    elif block == "monthly":
        interval = stock.monthly_time_series()
    else:
        return {"status": 400, "message": "Error"}

    # Check Key Name
    if key_group == "change":
        key_group = "Change Percentage"
    elif key_group == "open":
        key_group = "Open"
    elif key_group == "close":
        key_group = "Close"
    elif key_group == "volume":
        key_group = "Volume"
    else:
        return {"status": 400, "message": "Error"}

    # Data for plotting
    fig, ax = plt.subplots()
    fig.canvas.draw()

    x_vals = list()
    y_vals = list()
    for k in interval.keys():
        x_vals.append(datetime.datetime.strptime(k, '%Y-%m-%d'))
        y_vals.append(interval[k][key_group])

    ax.plot(x_vals, y_vals, color="red")

    fig.set_size_inches(12.5, 6.5, forward=True)
    ax.set(xlabel="Date", ylabel="{}".format(key_group))
    ax.legend(["{}".format(key_group)])

    filename = 'public/img/{0}{1}{2}Chart.png'.format(
        stock.symbol,
        key_group.upper().replace(" ", ""),
        block.upper()
    )

    plt.savefig(filename)

    return {"status": 200, "filename": filename}
