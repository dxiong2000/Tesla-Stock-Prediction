import pandas
from matplotlib import pyplot as plt
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from sklearn import tree
import graphviz

# HYPERPARAMETERS
LOSS = 'binary_crossentropy'
EPOCHS = 20
OPTIMIZER = 'adam'
BATCH_SIZE = 32


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

    return


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


def neural_net():
    df = pandas.read_csv('./data/train_test_samples.csv')
    X = df.X.tolist()
    y = df.y.tolist()

    # 75-25 train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=True)

    # create simple feed forward model
    model = Sequential()
    model.add(Dense(8, input_dim=1))
    model.add(Dense(8))
    model.add(Dense(4))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['accuracy', 'mean_squared_error', f1_m, precision_m, recall_m])
    model.fit(X_train, y_train, epochs=EPOCHS)
    history = model.fit(X_train, y_train, epochs=EPOCHS)

    loss, final_accuracy, mse, f1_score, precision, recall = model.evaluate(X_test, y_test)
    print('TEST ACCURACY:', final_accuracy)
    print('TEST PRECISION:', precision)
    print('TEST RECALL:', recall)
    print('TEST F1:', f1_score)

    # plot metrics
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

    y_pred = model.predict(X_test)
    for i,n in enumerate(y_pred):
        if n[0] < 0.5:
            y_pred[i][0] = 0
        else:
            y_pred[i][0] = 1
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return


def decision_tree():
    df = pandas.read_csv('./data/train_test_samples.csv')
    X = df.X.tolist()
    y = df.y.tolist()
    # 75-25 train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=True)
    model = DecisionTreeClassifier(max_depth=3)
    X_train = np.array(X_train).reshape(-1, 1)
    X_test = np.array(X_test).reshape(-1, 1)

    model = model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    #EXPORTING TREE AS PNG
    import os
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'

    dot_data = tree.export_graphviz(model, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.format = 'png'
    graph.render("tree")

    print('Decision Tree accuracy:', accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


def random_forest():
    df = pandas.read_csv('./data/train_test_samples.csv')
    X = df.X.tolist()
    y = df.y.tolist()
    # 75-25 train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=True)
    model = DecisionTreeClassifier(max_depth=3)
    X_train = np.array(X_train).reshape(-1, 1)
    X_test = np.array(X_test).reshape(-1, 1)

    randforest = RandomForestClassifier(max_depth=2, max_leaf_nodes=5)
    randforest = randforest.fit(X_train, y_train)
    y_pred = randforest.predict(X_test)

    print('Random Forest accuracy:', accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return


def naive_bayes():
    df = pandas.read_csv('./data/train_test_samples.csv')
    X = df.X.tolist()
    y = df.y.tolist()
    # 75-25 train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=True)
    X_train = np.array(X_train).reshape(-1, 1)
    X_test = np.array(X_test).reshape(-1, 1)

    gnb = GaussianNB()
    y_pred = gnb.fit(X_train, y_train).predict(X_test)

    print('Naive Bayes accuracy:', accuracy_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return


neural_net()
decision_tree()
random_forest()
naive_bayes()