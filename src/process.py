# Pre-process data for data mining and analysis
#
#
#
#

import pandas as pd
import GetOldTweets3 as got


#webscraper
def scrape_tweets():
    tweetCriteria = got.manager.TweetCriteria().setUsername("elonmusk").setSince("2010-06-28").setUntil("2020-05-27").setMaxTweets(0)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    tweet_list = [(tweet.id, tweet.permalink, tweet.username, tweet.to, tweet.text, tweet.date, tweet.retweets, tweet.favorites,
                   tweet.mentions, tweet.hashtags, tweet.geo) for tweet in tweets]
    df = pd.DataFrame(tweet_list, columns=['id', 'permalink', 'username', 'to', 'text', 'date', 'retweets', 'favorites', 'mentions', 'hashtags', 'geo'])
    df.to_csv('./data/elon_musk_tweets.csv', index=False)

#preprocessing of data
def process():
    df = pd.read_csv('./data/elon_musk_tweets.csv')

    #removes links in the string
    cleaned_text = []
    for index,row in df.iterrows():                                                                 
        words = [word for word in str(row.text).split() if "http" not in word]                  
        cleaned_text.append(' '.join(words))
    df['cleaned_text'] = cleaned_text


    #removes metions and the mentioned
    cleaned_text = []
    for index,row in df.iterrows():
        words = [word for word in str(row.cleaned_text).split() if "@" not in word]
        cleaned_text.append(' '.join(words))

    #create new column cleaned_text that is the version that doesnt have non-alphanumerics and NaN
    df['cleaned_text'] = cleaned_text
    df['cleaned_text'] = df['cleaned_text'].str.replace("[^a-zA-Z# ]", '')
    df = df[df['text'] != ' ']
    df = df[df['text'].notna()]
    df['cleaned_text'] = df['cleaned_text'].str.replace("\s+",' ')
    df = df[df['cleaned_text'] != ' ']
    df = df[df['cleaned_text'] != '']
    df = df[df['cleaned_text'].notna()]

    #creates new file called elon_musk_tweets_copy
    df.to_csv('./data/elon_musk_tweets_processed.csv', index=False)


process()