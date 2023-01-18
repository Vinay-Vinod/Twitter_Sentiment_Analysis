import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob 
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import re 
import numpy as np
import twitter_credentials
    

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


query = input("Enter person/topic of interest: ")
num_tweets = int(input("Enter number of tweets to analyze: "))
filtered = query + "-filter:retweets"

tweets = tweepy.Cursor(api.search_tweets, q=filtered, lang='en').items(num_tweets)

lst1 = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]

df = pd.DataFrame(data=lst1, columns=['tweets', 'user', 'locationl'])

tweet_lst = df.tweets.to_list()


def clean_tweet(tweet):
    if type(tweet) == np.float:
        return ""
    r = tweet.lower()
    r = re.sub("'", "", r) 
    r = re.sub("@[A-Za-z0-9_]+","", r)
    r = re.sub("#[A-Za-z0-9_]+","", r)
    r = re.sub(r'http\S+', '', r)
    r = re.sub('[()!?]', ' ', r)
    r = re.sub('\[.*?\]',' ', r)
    r = re.sub("[^a-z0-9]"," ", r)
    r = r.split()
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    r = [w for w in r if not w in stopwords]
    r = " ".join(word for word in r)
    return r

cleaned = [clean_tweet(tw) for tw in tweet_lst]

sen_obj = [TextBlob(tweet) for tweet in cleaned]
sen_obj[0].polarity, sen_obj[0]
sen_vals = [[tweet.sentiment.polarity, str(tweet)] for tweet in sen_obj]

sen_df = pd.DataFrame(sen_vals, columns=["polarity", "tweet"])

n = sen_df["polarity"]
m = pd.Series(n)
pos, neg, neu = 0, 0, 0

for items in m: 
    if items > 0:
        pos += 1
    elif items < 0:
        neg += 1
    else:
        neu += 1

pieLabels=["Positive Sentiment","Negative Sentiment","Neutral Sentiment"]

populationShare=[pos,neg,neu]

figureObject, axesObject = plt.subplots()

axesObject.pie(populationShare, labels=pieLabels,autopct='%1.2f',startangle=90)
axesObject.set_title("Sentiment Analysis of {}".format(query))

axesObject.axis('equal')


plt.show()
