import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def frequency():
    df = pd.read_csv('./data/elon_musk_tweets_processed.csv')
    date1, date2, date3, date4, date5, date6, date7, date8, date9, date10, date11 = (0, ) * 11

    for tweets in df.date:
        if "2020" in str(tweets):
            date11 += 1
        elif "2019" in str(tweets):
            date10 += 1
        elif "2018" in str(tweets):
            date9 += 1
        elif "2017" in str(tweets):
            date8 += 1
        elif "2016" in str(tweets):
            date7 += 1
        elif "2015" in str(tweets):
            date6 += 1
        elif "2014" in str(tweets):
            date5 += 1
        elif "2013" in str(tweets):
            date4 += 1
        elif "2012" in str(tweets):
            date3 += 1
        elif "2011" in str(tweets):
            date2 += 1
        elif "2010" in str(tweets):
            date1 += 1

    barWidth = 1

    datelist = [date1,date2,date3,date4,date5,date6,date7,date8,date9,date10,date11]
    for num in range(11):
        year = 2010
        plt.bar(num, datelist[num], width=barWidth, edgecolor='white', label=str(year+num))

    plt.xlabel('Year', fontweight='bold')
    plt.ylabel('Number of Tweets', fontweight='bold')
    plt.title('Elon Musk\'s Tweet Frequency')
    plt.xticks([r for r in range(11)], [ "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017","2018", "2019", "2020" ])
    plt.autoscale(tight=True)

    plt.show()


def sentiment_graph():
    df = pd.read_csv('./data/elon_musk_tweets_sentiments.csv')
    neg, neu, pos = (0,) * 3

    for value in df['polarity']:
        if value < -0.1:
            neg += 1
        elif value > 0.1:
            pos += 1
        else:
            neu += 1

    plt.subplot(111)
    w = 0.3
    plt.bar(0, neg, width=w, color='b', align='center')
    plt.bar(1, neu, width=w, color='g', align='center')
    plt.bar(2, pos, width=w, color='r', align='center')
    plt.autoscale(tight=True)

    plt.xlabel('Sentiment Value', fontweight='bold')
    plt.ylabel('Number of Tweets', fontweight='bold')
    plt.title('Sentiment Analysis Frequency')
    plt.xticks([r for r in range(3)], ["negative", "neutral", "positive"])
    plt.show()


frequency()
sentiment_graph()