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
    '''neg0, neu0, pos0 = (0, ) * 3
    neg1, neu1, pos1 = (0, ) * 3
    neg2, neu2, pos2 = (0, ) * 3
    neg3, neu3, pos3 = (0, ) * 3
    neg4, neu4, pos4 = (0, ) * 3
    neg5, neu5, pos5 = (0, ) * 3
    neg6, neu6, pos6 = (0, ) * 3
    neg7, neu7, pos7 = (0, ) * 3
    neg8, neu8, pos8 = (0, ) * 3
    neg9, neu9, pos9 = (0, ) * 3
    neg10, neu10, pos10 = (0, ) * 3'''

    neg, neu, pos = (0,) * 3

    for value in df['polarity']:
        if value < -0.1:
            neg += 1
        elif value > 0.1:
            pos += 1
        else:
            neu += 1

    '''    
    v2010 = [neg0, neu0, pos0]
    v2011 = [neg1, neu1, pos1]
    v2012 = [neg2, neu2, pos2]
    v2013 = [neg3, neu3, pos3]
    v2014 = [neg4, neu4, pos4]
    v2015 = [neg5, neu5, pos5]
    v2016 = [neg6, neu6, pos6]
    v2017 = [neg7, neu7, pos7]
    v2018 = [neg8, neu8, pos8]
    v2019 = [neg9, neu9, pos9]
    v2020 = [neg10, neu10, pos10]

    neg = [neg0, neg1, neg2, neg3, neg4, neg5, neg6, neg7, neg8, neg9, neg10]
    neu = [neu0, neu1, neu2, neu3, neu4, neu5, neu5, neu7, neu8, neu9, neu10]
    pos = [pos0, pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10]
    barWidth = 1

    plt.bar(0, neg, width=barWidth, edgecolor='white', align='center', label=str(2010))
    plt.bar(1, neu, width=barWidth, edgecolor='white', align='center', label=str(2011))
    plt.bar(2, pos, width=barWidth, edgecolor='white', align='center', label=str(2012))

    plt.bar(0, v2010, width=barWidth, edgecolor='white', align='center', label=str(2010))
    plt.bar(1, v2011, width=barWidth, edgecolor='white', align='center', label=str(2011))
    plt.bar(2, v2012, width=barWidth, edgecolor='white', align='center', label=str(2012))
    plt.bar(3, v2013, width=barWidth, edgecolor='white', align='center', label=str(2013))
    plt.bar(4, v2014, width=barWidth, edgecolor='white', align='center', label=str(2014))
    plt.bar(5, v2015, width=barWidth, edgecolor='white', align='center', label=str(2015))
    plt.bar(6, v2016, width=barWidth, edgecolor='white', align='center', label=str(2016))
    plt.bar(7, v2017, width=barWidth, edgecolor='white', align='center', label=str(2017))
    plt.bar(8, v2018, width=barWidth, edgecolor='white', align='center', label=str(2018))
    plt.bar(9, v2019, width=barWidth, edgecolor='white', align='center', label=str(2019))
    plt.bar(10, v2020, width=barWidth, edgecolor='white', align='center',label=str(2020))
    
    plt.xlabel('Sentiment Value', fontweight='bold')
    plt.ylabel('Number of Tweets', fontweight='bold')
    plt.title('Sentiment Analysis Frequency')
    plt.xticks([r for r in range(3)], [ "2010", "2011", "2012"])
'''
    ax = plt.subplot(111)
    w = 0.3
    ax.bar(0, neg, width=w, color='b', align='center')
    ax.bar(1, neu, width=w, color='g', align='center')
    ax.bar(2, pos, width=w, color='r', align='center')
    ax.autoscale(tight=True)

    plt.xlabel('Sentiment Value', fontweight='bold')
    plt.ylabel('Number of Tweets', fontweight='bold')
    plt.title('Sentiment Analysis Frequency')
    plt.xticks([r for r in range(3)], ["negative", "neutral", "positive"])
    plt.show()


frequency()
sentiment_graph()