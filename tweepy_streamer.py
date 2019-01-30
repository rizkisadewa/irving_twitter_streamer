from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

#class allow to create tweets
class StdOutListener(StreamListener):

    # the data that will be ontained from tweets and we can do what we want to that data
    def on_data(self, data):
        print(data)
        return True

    # will be over riding the error
    def on_error(self, status):
        print(status)

#create an object from StdOutListener
if __name__ == "__main__":

    listener = StdOutListener()
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)# this is an object from auth class that obtain the data from credentials file
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)# this is the method that we can access the token, obtain from the credentials file.

    stream = Stream(auth, listener)

    #dealling with the filter
    stream.filter(track=['joko widodo','prabowo subiyanto'])
