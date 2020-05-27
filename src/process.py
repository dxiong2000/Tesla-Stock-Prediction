# Pre-process data for data mining and analysis
#
#
#
#

import pandas as pd
import GetOldTweets3 as got
import numpy
'''
data = pd.read_excel(r'C:/Users/scott/OneDrive/Documents/UCSC/CSE145/Project/Tesla-Stock-Prediction/elonmusk1017.xlsx')
data = data[::-1]
data = data.reset_index(drop=True)
'''
tweetCriteria = got.manager.TweetCriteria().setUsername("elonmusk")\
                                           .setSince("2020-04-27")\
                                           .setUntil("2020-05-27")\
                                           .setMaxTweets(0)\
                                           .setEmoji("unicode")
tweet = got.manager.TweetManager.getTweets(tweetCriteria)
data = pd.DataFrame(tweet, columns = ['columns'])
data.to_csv('../Customer_Churn_processed.csv', index=False)