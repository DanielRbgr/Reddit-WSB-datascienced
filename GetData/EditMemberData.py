import pandas as pd
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef
from datetime import datetime

csvpath = "MemberData/Member_data.csv"

def printmemberfigure():
    # load the member data, interpolate the missing ones with linear method, round to remove decimal values
    df = pd.read_csv(csvpath, sep=';')
    df['date']= pd.to_datetime(df['date'], yearfirst=True)
    df['members'] = df['members'].interpolate().round(0)
    print(df.info)
    print(df.dtypes)

    #df.plot(x='date',y='members',kind='line')
    days=df['date']
    members=df['members']

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.plot(days, members/1000000, linewidth=2)
    plt.ylim([1, 10])
    ax.plot([datetime(2021, 1, 22), datetime(2021, 1, 22)], [1, 10], color='forestgreen',
                        alpha=0.8, label='2021-01-22', linestyle='dotted', linewidth=3.5)
    ax.plot([datetime(2021, 1, 29), datetime(2021, 1, 29)], [1, 10], color='midnightblue',
                        alpha=0.8, label='2021-01-29', linestyle='dotted', linewidth=3.5)
    ax.plot([datetime(2021, 2, 2), datetime(2021, 2, 2)], [1, 10], color='firebrick',
                        alpha=0.8, label='2021-02-02', linestyle='dotted', linewidth=3.5)
    ax.plot([datetime(2021, 2, 12), datetime(2021, 2, 12)], [1, 10], color='magenta',
                        alpha=0.8, label='2021-02-12', linestyle='dotted', linewidth=3.5)
    plt.title("Development of the Wallstreetbets members", fontdict=gdef.font_title, pad=20)
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.ylabel("Total members [in millions]", fontdict=gdef.font_label, labelpad=10)
    plt.grid()
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.legend(loc=2, fontsize='large')
    plt.subplots_adjust(bottom=0.2)

    for label in ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)

    plt.show()



printmemberfigure()