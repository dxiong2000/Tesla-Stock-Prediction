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

def stock_overtime():
    df_tesla = pd.read_excel('./data/TSLA.xlsx')
    df = df_tesla.iloc[729:751]
    df = df[::-1].reset_index().drop(columns=['index'])
    df['Adj Close'].plot(label='TSLA', title='Adjusted Closing Price for June 2017')
    plt.xlabel('date', fontweight='bold')
    plt.ylabel('closing price', fontweight='bold')
    plt.xticks([r for r in range(22)], ["2017-06-01",'','','','','','','','','','','','','','','','','','','','', "2017-06-30"])
    plt.show()

def sentiment_overtime():
    df_tweets = pd.read_csv('./data/elon_musk_tweets_sentiments.csv')
    df_tesla = pd.read_excel('./data/TSLA.xlsx')
    dates = []   
    for value in df_tweets['date']:
        dates.append(pd.Timestamp(value).tz_convert('America/New_York'))
    df_tweets['date'] = dates
    df_tweets = df_tweets.iloc[::-1].reset_index().drop(columns=['index'])
    
    dates = []
    for date in df_tesla.Date:
        dates.append(pd.Timestamp('{} 16:00:00-04:00'.format(str(date))))
    df_tesla['Date'] = dates
    df_tesla = df_tesla.iloc[::-1].reset_index().drop(columns=['index'])
    
    tweet_i = 2460
    tweet_entry = df_tweets.iloc[tweet_i]
    tesla_i = 1382
    df_t = df_tesla.iloc[1382:1404]

    X = []
    for stock_day in df_t.Date:
        polarity = 0
        n = 0
        while tweet_entry.date < stock_day:
            polarity += tweet_entry.polarity
            n += 1
            tweet_i += 1
            if tweet_i >= 2655:
                break
            tweet_entry = df_tweets.iloc[tweet_i]
        if n != 0:
            polarity = polarity/n
            X.append(polarity)

    plt.plot(X)
    plt.xlabel('Avg Sentiment', fontweight='bold')
    plt.ylabel('Date with Open Market', fontweight='bold')
    plt.title('Avg sentiment for June 2017', fontweight='bold')
    plt.xticks([r for r in range(19)], ["2017-06-01",'','','','','','','','','','','','','','','','','', "2017-06-30"])
    plt.show()
    
stock_overtime()
sentiment_overtime()
#frequency()
#sentiment_graph()