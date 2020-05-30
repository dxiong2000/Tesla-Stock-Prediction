import pandas
from textblob import TextBlob
from matplotlib import pyplot as plt


df = pandas.read_csv('./data/elon_musk_tweets_processed.csv')
polarity = []
subjectivity = []
for text in df.cleaned_text:
    tb = TextBlob(text)
    polarity.append(tb.sentiment.polarity)
    subjectivity.append(tb.sentiment.subjectivity)

df['polarity'] = polarity
df['subjectivity'] = subjectivity
df.to_csv('./data/elon_musk_tweets_sentiments.csv', index=False)

