from GetData.StockData  import GetStockData as gsd
import ProcessData.TitleFunctions as tf
import GlobalDefinitions as gdef
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def print_buzzword_stock_chart(buzzword, stock, start, end):

    start = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    df_buzzword = tf.display_buzzword(buzzword)
    df_stockprice = gsd.GetStockData(stock, start, end)
    # print(df_buzzword.shape)
    # print(df_stockprice.axes[0])


    df = pd.DataFrame(df_buzzword)
    x1 = pd.to_datetime(df.iloc[:, 0], unit='s') + pd.Timedelta('01:00:00')
    y1 = df.iloc[:, 1]
    x2 = df_stockprice.axes[0]
    y2 = df_stockprice['Close']
    fig, ax1 = plt.subplots(figsize=(12, 12))
    line1 = ax1.plot(x1, y1, '#CC0000', alpha=0.7, label='Mentions per day', marker='o')
    plt.ylabel("'GME' mentions per day", fontdict=gdef.font_label, labelpad=10)
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.grid()
    plt.ylim(0, 30000)
    #line3 = ax1.plot([datetime(2021, 1, 28), datetime(2021, 1, 28)], [0, 30000], color='k',
                        #alpha=0.7, label='Trade restricitions', linestyle='dotted')
    ax2 = ax1.twinx()
    line2 = ax2.plot(x2, y2, '#85bb65', linestyle='dashed', label='Stock price', marker='o')
    plt.title("'GME' mentions per day and stock price", fontdict=gdef.font_title, pad=20)
    plt.ylabel("'GME' stock price [$]", fontdict=gdef.font_label, labelpad=10)

    lns = line1 + line2 #+ line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0, fontsize='large')

    plt.show()

print_buzzword_stock_chart("GME", "GME", gdef.firsttimstamp, gdef.endtime)



