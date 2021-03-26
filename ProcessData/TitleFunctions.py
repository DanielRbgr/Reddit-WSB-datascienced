import os, TextFunctions, MemberData
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef
import re

def load_csv_data():
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/datasets/CSVfiles/datadump_sorted_WithNames.csv")
    # separation by semicolon is really important
    df = pd.read_csv(filepath, sep=';')
    return df

def print_dataframe(dataframe, title, lblxaxis, lblyaxis, legend):

    # df.plot(x='date',y='members',kind='line')
    df = pd.DataFrame(dataframe)
    x = pd.to_datetime(df.iloc[:, 0], unit='s') + pd.Timedelta('01:00:00')
    y = df.iloc[:, 1]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.plot(x, y, 'r')
    plt.title(title, fontdict=gdef.font_title, pad=20)
    plt.ylabel(lblyaxis, fontdict=gdef.font_label)
    plt.xlabel(lblxaxis, fontdict=gdef.font_label)
    plt.legend([legend])
    plt.grid()

    plt.show()

orig_df = load_csv_data()

def count_buzzwords(start, end, buzzword):

    #print("Full dataframe shape: " + str(df.shape))

    # Aufbau der CSV: ['utc', 'title', 'author', 'url']
    booldf = ((orig_df['utc'] >= start) & (orig_df['utc'] <= end))
    # print("Number of Post in this period of time: " + str(booldf.sum()))

    df = orig_df[booldf]
    #print("Remaining dataframe shape: " + str(df.shape))

    counter = 0

    for title in df['title']:
        if buzzword.lower() in TextFunctions.remove_emojys(title).lower():
            counter = counter + 1
        #print(TextFunctions.remove_emojys(title))

    return counter

def display_buzzword(buzzword):
    starttime = gdef.firsttimstamp
    daily_buzzwords = pd.DataFrame(columns=['day', 'mentions'])

    while datetime.fromtimestamp(starttime) < gdef.endtime:
        count = count_buzzwords(starttime, starttime+gdef.timeticksperday-1, buzzword)
        daily_buzzwords.loc[len(daily_buzzwords.day)] = [starttime, count]
        #print(datetime.fromtimestamp(starttime))
        #print(count)
        starttime = starttime + gdef.timeticksperday

    #print(daily_buzzwords)
    daily_buzzwords.replace(0, np.nan, inplace=True)
    daily_buzzwords['mentions'] = daily_buzzwords['mentions'].interpolate()
    return daily_buzzwords


"""
def count_all_words():

    df = orig_df

    df_allwords = pd.DataFrame(columns=['word', 'count'])
    allwords_dic = {}

    # this code wroks aswell, but it needs WAY WAY longer than with the dictionarys (16h vs 5min)
    # thus, it's here just for research/whatever reasons
    #for title in df['title']:
    #    title =  TextFunctions.remove_emojys(title).lower()
    #    title = title.split(" ")
    #    for word in title:
    #        word = re.sub('[^a-zA-Z]+', '', word)
    #        print(sum(df_allwords['word'].isin([word])))
    #        if sum(df_allwords['word'].isin([word])) != 0 :
    #            index = df_allwords.loc[df_allwords['word']==word].index
    #            print(index.values[0])
    #            df_allwords.iloc[index.values[0], 1] = df_allwords.iloc[index.values[0], 1] + 1
    #        else:
    #            df_allwords.loc[len(df_allwords)] = [word, 1]

    #return df_allwords
    

    for title in df['title']:
        title = TextFunctions.remove_emojys(title).lower()
        title = title.split(" ")
        for word in title:
            word = re.sub('[^a-zA-Z]+', '', word)
            print(word in allwords_dic.keys())
            if word in allwords_dic.keys():
                allwords_dic[word] = allwords_dic[word] + 1
            else:
                allwords_dic[word] = 1

    df_allwords = pd.DataFrame().from_dict(allwords_dic.items())

    return df_allwords

df = count_all_words()
df.to_csv('allwords.csv', index=False)
"""
print(df)

# -------------------------Printing the graph of a single stock------------------------------------
"""
print_dataframe(display_buzzword("BB"), "Mentions of 'BB' per day", "Date", "Mentions", "BB")
"""

# -------------------------Printing graph of multiple buzzwords------------------------------------
"""
df_gme = display_buzzword("GME")
df_bb = display_buzzword("AMC")
df_amc = display_buzzword("BB")

# df.plot(x='date',y='members',kind='line')
df = df_gme
x = pd.to_datetime(df.iloc[:, 0], unit='s') + pd.Timedelta('01:00:00')
y = list(df.iloc[:, 1])
y2 = list(df_bb.iloc[:, 1])
y2 = np.add(y2, y)
y3 = list(df_amc.iloc[:, 1])
y3 = np.add(y3, y2)
fig, axs = plt.subplots(figsize=(12, 12))
axs.bar(x, y,   color='#EE2622', label='GME', zorder=3)
axs.bar(x, y2,  color='g', label='AMC', zorder=2)
axs.bar(x, y3, color='b', label='BB', zorder=1)

plt.title("Titel", fontdict=gdef.font_title, pad=20)
plt.ylabel("YLabel", fontdict=gdef.font_label, labelpad=10)
plt.xlabel("XLabel", fontdict=gdef.font_label, labelpad=10)
plt.legend()
plt.grid()

plt.show()
"""

