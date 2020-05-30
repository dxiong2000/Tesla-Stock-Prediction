import pandas
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split


# HYPERPARAMETERS
LOSS = 'binary_crossentropy'
EPOCHS = 25
OPTIMIZER = 'adam'


def preprocess():
    df_tweets = pandas.read_csv('./data/elon_musk_tweets_sentiments.csv')
    df_tesla = pandas.read_excel('./data/TSLA.xlsx')

    # df of dates and polarities
    df_tweets = df_tweets.drop(columns=['id', 'permalink', 'username', 'to', 'text', 'retweets', 'favorites', 'mentions',
                                        'hashtags', 'geo', 'cleaned_text'])
    df_tesla = df_tesla.drop(columns=['High', 'Low', 'Adj Close', 'Volume'])

    # assigns 0 for decrease in stock performance, 1 for increase
    perf = [int(day_close - day_open > 0) for day_open, day_close in zip(df_tesla.Open, df_tesla.Close)]
    df_tesla = df_tesla.drop(columns=['Open', 'Close'])
    df_tesla['perf'] = perf

    # convert UTC to EST in accordance with NYSE hours
    dates = []
    for date in df_tweets.date:
        dates.append(pandas.Timestamp(date).tz_convert('America/New_York'))
    df_tweets['date'] = dates

    # add market close time to date
    dates = []
    for date in df_tesla.Date:
        dates.append(pandas.Timestamp('{} 16:00:00-04:00'.format(str(date))))
    df_tesla['Date'] = dates

    # reverse data frames so they are in chronological order
    df_tweets = df_tweets.iloc[::-1].reset_index().drop(columns=['index'])
    df_tesla = df_tesla.iloc[::-1].reset_index().drop(columns=['index'])

    # print(df_tweets.head(10))
    # print(df_tesla.head(10))

    # dates are in YMD format, mon = 0, fri = 4
    tweet_i = 0
    tweet_entry = df_tweets.iloc[tweet_i]
    X = []
    y = []
    for stock_day, perf in zip(df_tesla.Date, df_tesla.perf):
        polarity = 0
        n = 0
        while tweet_entry.date < stock_day:
            polarity += tweet_entry.polarity
            n += 1
            tweet_i += 1
            if tweet_i >= len(df_tweets):
                break
            tweet_entry = df_tweets.iloc[tweet_i]

        if n != 0:
            polarity = polarity/n
            X.append(polarity)
            y.append(perf)

    df = pandas.DataFrame(list(zip(X, y)), columns=['X', 'y'])
    df.to_csv('./data/train_test_samples.csv')


def neural_net():
    df = pandas.read_csv('./data/train_test_samples.csv')
    X = df.X.tolist()
    y = df.y.tolist()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=True)

    model = Sequential()
    model.add(Dense(16, input_dim=1, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(2, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['accuracy', 'mean_squared_error'])
    history = model.fit(X_train, y_train, epochs=EPOCHS)

    _, final_accuracy, _ = model.evaluate(X_test, y_test)
    print('TEST ACCURACY:', final_accuracy)

    # plot
    plt.plot(history.history['accuracy'])
    plt.title('Accuracy over Epochs')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.show()

    plt.plot(history.history['mean_squared_error'])
    plt.title('MSE over Epochs')
    plt.ylabel('MSE')
    plt.xlabel('Epoch')
    plt.show()


neural_net()