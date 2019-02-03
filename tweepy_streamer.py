from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np #library for process the number, math or etc.
import pandas as pd #library for analyze
import matplotlib.pyplot as plt #library for print the grafik of the data


### TWITTER CLIENT ###
class TwitterClient():

    def __init__(self, twitter_user=None):
        # twitter_user=None : if we do not input the parameter, then we will see our own timeline

        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user # declaration of the parameter twitter_user

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
            home_timeline.append(tweet)
        return home_timeline_tweets

    ## we can view the lst of the scope in twitter in this link http://docs.tweepy.org/en/v3.5.0/api.html for references

## TWITTER AUTHENTICATOR ###
## the class that handle authentication
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)# this is an object from auth class that obtain the data from credentials file
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)# this is the method that we can access the token, obtain from the credentials file.
        return auth


# TWITTER STREAMMER : class who responsible for tweet
class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    """
    Class for streaming and processing live tweets.
    fetch_tweets_filename is for the parameter that we can print into the file
    hash_tag_list is for the keyword of hashtag
    """
    def stream_tweet(self, fetched_tweets_filename, hash_tag_list):
        # this handles Twitter Authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener(fetch_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        #dealling with the filter use a paramte from this function
        stream.filter(track=hash_tag_list)



# TWITTER STREAM LISTENER : class allow to create tweets
class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """

    # a constructor
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # the data that will be ontained from tweets and we can do what we want to that data
    def on_data(self, data):
        try:
            print(data)
            #write tweets into the file
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    # will be over riding the error
    def on_error(self, status):

        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

class TwitterAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        # DataFrame() is a function built in pandas to make a Data Frame.
        # tweet.text for tweet in tweets we loop all the tweets and set as a data.

        df['id'] = np.array([tweet.id for tweet in tweets]) # make another column for an id of the tweets
        df['len'] = np.array([len(tweet.text) for tweet in tweets]) # make another column for long of tweets
        df['date'] = np.array([tweet.created_at for tweet in tweets]) # make another column for tweets date of creation
        df['source'] = np.array([tweet.source for tweet in tweets]) # make another column for the kind of device source tweets made
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets]) # make another column for like of the tweets
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets]) # make another column for tweets date of creation

        return df

#create an object from StdOutListener
if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TwitterAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    # user_timeline above is not the function that we declared, this is a function from Twitter API


    # # if we would like to know what the data will be shorted by certain category such as id and retweet count, below the function
    # print(dir(tweets[0]))
    # print(tweets[0].id)
    # print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    # print(df.head(10))

    # Get average length over all tweets
    print("Sample : %s" % np.mean(df['len'])) #mean() is the function mean from numpy

    # Get the number of likes for the most liked tweet.
    print("The number of likes for the most liked tweet : %s" % np.max(df['likes']))

    # Get the number of retweets for the most retweeted tweet.
    print("The number of retweets for the most retweeted tweet : %s" % np.max(df['retweets']))

    # # Option 1 : make a plot in Time Series for number of likes and the date
    # time_likes = pd.Series(data=df['likes'].values, index=df['date']) #y axes is by likes, x axes is by the date
    # time_likes.plot(figsize=(16, 4), color='r') #picture in 16 inc and 4 inc with color red
    # plt.show()

    # # Option 2 : make a plot in Time Series for number of retweets and the date
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date']) #y axes is by retweets, x axes is by the date
    # time_retweets.plot(figsize=(16, 4), color='r') #picture in 16 inc and 4 inc with color red
    # plt.show()

    # Option 3 : make a plot in Time Series for number of retweets, number of likes and the date
    time_likes = pd.Series(data=df['likes'].values, index=df['date']) #y axes is by likes, x axes is by the date
    time_likes.plot(figsize=(16, 4), label='likes', legend=True) #picture in 16 inc and 4 inc with color red

    time_retweets = pd.Series(data=df['retweets'].values, index=df['date']) #y axes is by retweets, x axes is by the date
    time_retweets.plot(figsize=(16, 4), label='retweets', legend=True) #picture in 16 inc and 4 inc with color red

    plt.show() #show the graphic
