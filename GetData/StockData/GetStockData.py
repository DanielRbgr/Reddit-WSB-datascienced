import yfinance as yf

def GetStockData(ticker, per_start, per_end):

    #define the ticker symbol
    tickerSymbol = ticker

    #get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    #get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start=per_start, end=per_end)

    #see your data
    # print(tickerDf)
    return tickerDf

