"""
This file covers all functions related to the sentiment of Reddit posts
This includes:
    - getting a sentiment score for a single sentence
    - analyze the sentiment score for a timeframe
    - load sentiment score from a csv
    - exp_sentiment: access the sentiment scores of a certain file from another file system
"""
from textblob import TextBlob
import ProcessData.TitleFunctions as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import TextFunctions
import GlobalDefinitions as gdef
from datetime import datetime

orig_df = tf.load_csv_data()
starttime = gdef.firsttimstamp
endtime = 1617141600


def get_sentiment(start, end, keyword):

    booldf = ((orig_df['utc'] >= start) & (orig_df['utc'] <= end))
    # print("Number of Post in this period of time: " + str(booldf.sum()))
    df = orig_df[booldf]

    df_sentiment = pd.DataFrame(columns=['polarity'])

    for title in df['title']:

        title= TextFunctions.remove_emojys(title).lower()

        if keyword == "":
            df_sentiment.loc[len(df_sentiment)] = TextBlob(title).sentiment.polarity
        else:
            if keyword.lower() in title:
                df_sentiment.loc[len(df_sentiment)] = TextBlob(title).sentiment.polarity

    return df_sentiment

def analyze_sentiment(start, end, keyword):

    df_sentiment = pd.DataFrame(columns=['date', 'polarity_tot', 'polarity_mean'])

    while start < end:
        df_daysent = get_sentiment(start, start + gdef.timeticksperday, keyword)
        df_sentiment.loc[len(df_sentiment)] = [int(start), df_daysent.polarity.sum(), df_daysent.polarity.mean()]
        print(df_sentiment.shape)
        start = start + gdef.timeticksperday

    return df_sentiment

def load_sentiment():
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/SentimentData/AMC_Sentiment.csv")
    df_sentiment = pd.read_csv(filepath, usecols=[1, 2, 3], header=0)
    df_sentiment['polarity_tot'].replace(0.0, np.nan, inplace=True)
    df_sentiment['polarity_tot'] = df_sentiment['polarity_tot'].interpolate()
    df_sentiment['polarity_mean'] = df_sentiment['polarity_mean'].interpolate()
    df_sentiment.date = df_sentiment.date.astype('int32')
    df_sentiment.date = pd.to_datetime(df_sentiment.date, unit='s') + pd.Timedelta('01:00:00')
    """
    # Had doubt about the mean sentiment, but calculation is correct
    df_count = tf.display_buzzword("GME", starttime)
    df_count.day = pd.to_datetime(df_count.day, unit='s') + pd.Timedelta('01:00:00')
    df_count['mentions'].replace(np.nan, 0.0, inplace=True)
    df_count.mentions = df_count.mentions.astype('int32')

    df_sentiment['polarity_mean2'] = df_sentiment['polarity_tot'].div(df_count['mentions'])
    """
    ylim = [-0.16, 0.4]
    fig, ax1 = plt.subplots(figsize=(12, 12))
    # total is mediumblue, mean is goldenrod
    line1 = ax1.plot(df_sentiment.date, df_sentiment.polarity_tot, label='"GME" total sentiment', color='cornflowerblue',
             linewidth=2)
    plt.ylabel("Total Sentiment Score", fontdict=gdef.font_label, labelpad=10)
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.grid(zorder=0)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.title('Sentiment for "GME" posts', fontdict=gdef.font_title, pad=20)
    ax2 = ax1.twinx()
    line2 = ax2.bar(df_sentiment.date, df_sentiment.polarity_mean, alpha=0.6, color='goldenrod', label='"GME" mean sentiment')
    line3 = ax2.plot([datetime(2021, 1, 28), datetime(2021, 1, 28)], ylim, color='k', linewidth='2',
             label='Trade restricitions', alpha=0.8, linestyle='dotted')
    plt.ylabel("Mean Sentiment Score", fontdict=gdef.font_label, labelpad=10)
    plt.ylim(ylim)
    plt.yticks(fontsize='xx-large')

    lns = line1 + [line2] + line3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=2, fontsize='xx-large')

    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)
    plt.show()

def exp_sentiment():

    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/SentimentData/GME_Sentiment.csv")
    df_sentiment = pd.read_csv(filepath, usecols=[1, 2, 3], header=0)
    df_sentiment['polarity_tot'].replace(0.0, np.nan, inplace=True)
    df_sentiment['polarity_tot'] = df_sentiment['polarity_tot'].interpolate()
    df_sentiment['polarity_mean'] = df_sentiment['polarity_mean'].interpolate()
    df_sentiment.date = df_sentiment.date.astype('int32')
    df_sentiment.date = pd.to_datetime(df_sentiment.date, unit='s') + pd.Timedelta('01:00:00')

    return df_sentiment

load_sentiment()
#df_sentiment = analyze_sentiment(starttime, endtime, "AMC")
#df_sentiment.to_csv("amc_Sentiment.csv")