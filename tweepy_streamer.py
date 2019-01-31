from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

### TWITTER CLIENT ###
class TwitterClient():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

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

#create an object from StdOutListener
if __name__ == "__main__":

    #create a hashtag
    hash_tag_list = ["joko widodo", "Prabowo Subianto", "Susi Puji Astuti"]

    #create the variable to make a file so that will be given the name, for below only for json format
    #if you would like to have another format, just edit .json format into .txt or etc.
    fetch_tweets_filename = "tweets.json"

    ## Make a twitter client object
    twitter_client = TwitterClient()
    print(twitter_client.get_user_timeline_tweets(1))

    # # make a twitter streamer object
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweet(fetch_tweets_filename, hash_tag_list)
