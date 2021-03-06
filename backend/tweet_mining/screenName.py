from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
from translation import (set_default_translation, set_default_language,set_default_proxies, get, ConnectError)


class TwitterClient():
    def __init__(self, twitter_user=None,hash_tag_list=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user
        self.hash_tag_list = hash_tag_list

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TweetAnalyzer():

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        # df['len'] = np.array([len(tweet.text) for tweet in tweets])
        # df['date'] = np.array([tweet.created_at for tweet in tweets])
        # df['source'] = np.array([tweet.source for tweet in tweets])
        # df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        # df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="PMOIndia" , lang = 'en', count=10)
    df = tweet_analyzer.tweets_to_data_frame(tweets)

    tweets = []

    for column in df[['tweets']]:
        columnSeriesObj = df[column]
        tweets = columnSeriesObj.values

    for tweet in tweets:
        tweet = tweet.replace(',', '')
        tweet = tweet.strip()
        print(tweet)

    df.to_csv('../data/mined.csv', index=False)
    print(df.head(100))