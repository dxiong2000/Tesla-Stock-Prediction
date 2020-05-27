# Pre-process data for data mining and analysis
#
#
#
#

import pandas as pd
import GetOldTweets3 as got
import numpy


def scrape_tweets():
    tweetCriteria = got.manager.TweetCriteria().setUsername("elonmusk").setSince("2010-06-28").setUntil("2020-05-27").setMaxTweets(0)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    tweet_list = [(tweet.id, tweet.permalink, tweet.username, tweet.to, tweet.text, tweet.date, tweet.retweets, tweet.favorites,
                   tweet.mentions, tweet.hashtags, tweet.geo) for tweet in tweets]
    df = pd.DataFrame(tweet_list, columns=['id', 'permalink', 'username', 'to', 'text', 'date', 'retweets', 'favorites', 'mentions', 'hashtags', 'geo'])
    df.to_csv('elon_musk_tweets.csv', index=False)


def process():
    df = pd.read_csv('elon_musk_tweets_copy.csv')
    for post in df['text']:
        for char in post
