"""
This file covers all functions related to the stock price
This includes:
    - printing a chart with buzzword count and stock price
"""
from GetData.StockData  import GetStockData as gsd
import ProcessData.TitleFunctions as tf
import GlobalDefinitions as gdef
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

max_y_scale = 400

def plot_buzzword_stock_chart(buzzword, stock, start, end):
    # buzzword needs start time in unix time format
    df_buzzword = tf.display_buzzword(buzzword, start, end)
    # stock data need start time as str
    start = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d')
    end = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d')
    df_stockprice = gsd.GetStockData(stock, start, end)

    df = pd.DataFrame(df_buzzword)
    x1 = pd.to_datetime(df.iloc[:, 0], unit='s') + pd.Timedelta('01:00:00')
    y1 = df.iloc[:, 1]
    x2 = df_stockprice.axes[0]
    y2 = df_stockprice['Close']
    fig, ax1 = plt.subplots(figsize=(12, 12))
    line1 = ax1.plot(x2, y2, color='darkgreen', label='Stock price', zorder=3, linewidth=4)
    ylabel = stock + " stock price [$]"
    plt.ylabel(ylabel, fontdict=gdef.font_label, labelpad=10)
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.grid(zorder=0)
    plt.ylim(0, max_y_scale) # change range of stock price chart to correct values
    ax2 = ax1.twinx()
    line2 = ax2.bar(x1, y1, color='firebrick', label='Mentions per day', zorder=5)
    title = buzzword + " mentions per day and stock price"
    plt.title(title, fontdict=gdef.font_title, pad=20)
    ylabel = buzzword + " mentions per day"
    plt.ylabel(ylabel, fontdict=gdef.font_label, labelpad=10)
    line3 = ax1.plot([datetime(2021, 1, 28), datetime(2021, 1, 28)], [0, 30000], color='k', linewidth='2',
                        label='Trade restricitions')
    plt.yticks(fontsize='xx-large')

    lns = line1 + [line2] + line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0, fontsize='xx-large')

    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)
    plt.show()

if __name__ == '__main__':
    # using the unix timestamp 1609455600 (1.1.2021 00:00:00), as nothing before January is of interest
    plot_buzzword_stock_chart("AMC", "AMC", gdef.firsttimstamp, gdef.lasttimestamp)



