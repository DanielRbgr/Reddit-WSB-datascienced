import yfinance as yf

def GetStockData(ticker, per_start, per_end):

    #define the ticker symbol
    ticker_symbol = ticker

    #get data on this ticker
    ticker_data = yf.Ticker(ticker_symbol)

    #get the historical prices for this ticker
    ticker_df = ticker_data.history(period='1d', start=per_start, end=per_end)

    #see your data
    # print(ticker_df)
    return ticker_df

