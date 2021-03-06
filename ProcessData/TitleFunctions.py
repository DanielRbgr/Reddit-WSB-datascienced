"""
This file includes all functions necessary evaluate the post titles
This includes:
    - loading the posts
    - search a certain timeframe for a buzzword (any timeframe)
    - display the mentions of buzzwords over a certain timeframe (in 1d steps)
    - various code blocks to evaluate and show plots
"""
import os, TextFunctions, MemberData
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef
import re

# ----------------------------------------------basic functions--------------------------------------------------------
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
    ax.bar(x, y, color='brown', zorder=2)
    plt.title(title, fontdict=gdef.font_title, pad=20)
    plt.ylabel(lblyaxis, fontdict=gdef.font_label)
    plt.xlabel(lblxaxis, fontdict=gdef.font_label)
    plt.xticks(fontsize="xx-large")
    plt.yticks(fontsize="xx-large")
    #plt.ylim(0, 20000)
    plt.legend([legend], fontsize="xx-large")
    plt.grid(zorder=0)

    plt.show()

def count_buzzwords(start, end, buzzword):

    orig_df = load_csv_data()

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

def display_buzzword(buzzword, start, end):
    starttime = start
    daily_buzzwords = pd.DataFrame(columns=['day', 'mentions'])

    while datetime.fromtimestamp(starttime) < datetime.fromtimestamp(end):
        count = count_buzzwords(starttime, starttime+gdef.timeticksperday-1, buzzword)
        daily_buzzwords.loc[len(daily_buzzwords.day)] = [starttime, count]
        #print(datetime.fromtimestamp(starttime))
        #print(count)
        starttime = starttime + gdef.timeticksperday

    #print(daily_buzzwords)
    daily_buzzwords.replace(0, np.nan, inplace=True)
    daily_buzzwords['mentions'] = daily_buzzwords['mentions'].interpolate()
    return daily_buzzwords

# -------------------------------counting all words in the titles------------------------------------------------------
def count_all_words():

    df = load_csv_data()

    df_allwords = pd.DataFrame(columns=['word', 'count'])
    allwords_dic = {}

    # this code works as well, but it needs WAY WAY longer than with the dictionarys (16h vs 5min)
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

# -------------------------------working with the title word count-----------------------------------------------------
def plot_top_ten_words():
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/datasets/CSVfiles/all_words_count.csv")
    # separation by semicolon is really important
    df = pd.read_csv(filepath, sep=',', names=['word', 'count'])
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)
    df = df.drop([0])

    # for showing the top 15 words
    # df2 = df.iloc[0:15, :].sort_values(by='count', ascending=True)

    # for showing the 10 most mentioned- short squeeze related words
    # the rows were selected by hand on basis of what i found interesting
    df2 = pd.DataFrame(columns=['word', 'count'])
    df2 = df2.append(df.loc[3, :])
    df2 = df2.append(df.loc[14, :])
    df2 = df2.append(df.loc[15, :])
    df2 = df2.append(df.loc[19, :])
    df2 = df2.append(df.loc[22, :])
    df2 = df2.append(df.loc[25, :])
    df2 = df2.append(df.loc[29, :])
    df2 = df2.append(df.loc[50, :])
    df2 = df2.append(df.loc[55, :])
    df2 = df2.sort_values(by='count', ascending=True)

    fig, ax = plt.subplots()
    ax.barh(df2.iloc[:, 0], df2.iloc[:, 1], align='center', color='firebrick', zorder=3)
    plt.grid(zorder=0)
    plt.xlabel('Number of mentions', fontdict=gdef.font_label, labelpad=10)
    plt.title('Most mentioned short squeeze related words in post titles', fontdict=gdef.font_title, pad=20)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')

    plt.show()


# -------------------------------Printing graph of multiple buzzwords--------------------------------------------------
def plot_stockmentions_per_day():
    df_gme = display_buzzword("GME", gdef.firsttimstamp, gdef.lasttimestamp)
    df_amc = display_buzzword("AMC", gdef.firsttimstamp, gdef.lasttimestamp)
    df_nok = display_buzzword("NOK", gdef.firsttimstamp, gdef.lasttimestamp)
    df_bb = display_buzzword("BB", gdef.firsttimstamp, gdef.lasttimestamp)

    x = pd.to_datetime(df_gme.iloc[:, 0], unit='s') + pd.Timedelta('01:00:00')
    y = list(df_gme.iloc[:, 1])
    y2 = list(df_amc.iloc[:, 1])
    y2 = np.add(y2, y)
    y3 = list(df_nok.iloc[:, 1])
    y3 = np.add(y3, y2)
    y4 = list(df_bb.iloc[:, 1])
    y4 = np.add(y4, y3)
    fig, axs = plt.subplots(figsize=(12, 12))
    axs.bar(x, y,   color='#EE2622', label='GME', zorder=6)
    axs.bar(x, y2,  color='seagreen', label='AMC', zorder=5)
    axs.bar(x, y3, color='midnightblue', label='NOK', zorder=4)
    axs.bar(x, y4, color='dimgray', label='BB', zorder=3)

    plt.title("Distribution of top 4 mentioned stocks", fontdict=gdef.font_title, pad=20)
    plt.ylabel("Mentions", fontdict=gdef.font_label, labelpad=10)
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.legend(loc=2, fontsize='xx-large')
    plt.grid(zorder=0)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')

    plt.show()

if __name__ == '__main__':
    print_dataframe(display_buzzword("gme", gdef.firsttimstamp, 1617141600), "Mentions of 'GME' per day",
                    "Date", "Mentions", "GME mentions")
    # df = count_all_words()
    # df.to_csv('allwords.csv', index=False)