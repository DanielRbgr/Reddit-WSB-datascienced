import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef

def load_csv_data():
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/datasets/CSVfiles/datadump_sorted_WithNames.csv")
    # separation by semicolon is really important
    df = pd.read_csv(filepath, sep=';')
    return df

orig_df = load_csv_data()

# -------------------------Printing the total number of comments------------------------------------

x = []
y = []
starttime = gdef.firsttimstamp

while datetime.fromtimestamp(starttime) <= gdef.endtime:
    booldf = ((orig_df['utc'] >= starttime) & (orig_df['utc'] <= starttime + gdef.timeticksperday))
    x.append((datetime.utcfromtimestamp(starttime) + timedelta(hours=1)).strftime('%Y-%m-%d'))
    y.append(sum(booldf))
    starttime = starttime + gdef.timeticksperday

print(x)
print(y)
# interpolating the data so that the missing dates are filled
df = pd.DataFrame(y, columns=['count'])
df.replace(0, np.NaN, inplace=True)
y2 = df['count'].interpolate(method='linear')
fig, axs = plt.subplots(figsize=(12, 12))
plt.bar(x, y2/1000, align='center', alpha=0.5)
plt.title("Total number of comments", fontdict=gdef.font_title, pad=20)
plt.ylabel("Count [in thousand]", fontdict=gdef.font_label, labelpad=10)
plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
plt.xticks(x[0:-1:14])
plt.grid()
plt.show()


"------------------------Standardized comment cound an whateverstock price-------------------------------------------"
"""
df_totalcom = pd.DataFrame(columns=['date', 'count'])
starttime = gdef.firsttimstamp

while datetime.fromtimestamp(starttime) < gdef.endtime:
    booldf = ((orig_df['utc'] >= starttime) & (orig_df['utc'] <= starttime + gdef.timeticksperday))
    x = (datetime.utcfromtimestamp(starttime) + timedelta(hours=1)).strftime('%Y-%m-%d')
    y = sum(booldf)
    df_totalcom.loc[len(df_totalcom)] = [x, y]
    starttime = starttime + gdef.timeticksperday


df_totalcom['count'].replace(0, np.NaN, inplace=True)
df_totalcom['count'] = df_totalcom['count'].interpolate()
fig, axs = plt.subplots(figsize=(12, 12))
axs.bar(df_totalcom['date'], df_totalcom['count'] / df_totalcom['count'].max(), align='center', alpha=0.5)
plt.title("Number of comments and GME stock price (standardized)", fontdict=gdef.font_title, pad=20)
plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
plt.xticks(df_totalcom.iloc[::14, 0], fontsize='large')
plt.yticks(fontsize='large')
plt.grid(axis='y')

start = datetime.utcfromtimestamp(gdef.firsttimstamp).strftime('%Y-%m-%d')
end = gdef.endtime.strftime('%Y-%m-%d')
df_stockprice = gsd.GetStockData("GME", start, end)
df_stockprice = df_stockprice.iloc[1:]
axs.plot(df_stockprice.axes[0].strftime('%Y-%m-%d'), df_stockprice['Close']/df_stockprice['Close'].max())

plt.show()
"""