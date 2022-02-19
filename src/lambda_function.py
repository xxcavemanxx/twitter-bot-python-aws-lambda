import os
import random
import json
from pathlib import Path
import tweepy
import csv


ROOT = Path(__file__).resolve().parents[0]


def lambda_handler(event, context):
    print("Authenticate")

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    # access_token = os.getenv("ACCESS_TOKEN")
    # access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=consumer_key,
        redirect_uri="http://172.17.0.1/twitter_callback.php",
        scope=["tweet.read", "users.read"],
        # Client Secret is only necessary if using a confidential client
        client_secret=consumer_secret
    )

    print(oauth2_user_handler.get_authorization_url())

    access_token = oauth2_user_handler.fetch_token(
        "Authorization Response URL here"
    )

    client = tweepy.Client(access_token)




    # auth = get_auth()
    # api = tweepy.API(auth)
    #
    # print("Get accounts to monitor from csv file")
    # monitor_accs_fname = ROOT / "monitor_accounts.csv"
    #
    # # monitor_accs = get_accs_to_monitor(monitor_accs_fname)
    #
    # consumer_key = os.getenv("CONSUMER_KEY")
    # consumer_secret = os.getenv("CONSUMER_SECRET")
    # access_token = os.getenv("ACCESS_TOKEN")
    # access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    #
    # print("Monitoring tweets")
    # tweet_stream = TweetStream(consumer_key, consumer_secret, access_token, access_token_secret)
    # tweet_stream.filter(follow=['Tyler_2112'])
    # stream_thread = tweet_stream.filter(follow=['gary_vee'], threaded=True)

    # print("Printing tweet IDs")
    # printer = IDPrinter(consumer_key, consumer_secret, access_token, access_token_secret)
    # printer.sample()

    # recent_tweets = api.user_timeline()[:3]
    # tweet = get_tweet(monitor_accs_fname)
    #
    # print(f"Post tweet: {tweet}")
    # api.update_status(tweet)

    # return {"statusCode": 200, "tweet": tweet}
    return {"statusCode": 200}


def get_auth():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


def get_tweet(tweets_file, excluded_tweets=None):
    """Get tweet to post from CSV file"""

    with open(tweets_file) as csvfile:
        reader = csv.DictReader(csvfile)
        possible_tweets = [row["tweet"] for row in reader]

    if excluded_tweets:
        recent_tweets = [status_object.text for status_object in excluded_tweets]
        possible_tweets = [tweet for tweet in possible_tweets if tweet not in recent_tweets]

    selected_tweet = random.choice(possible_tweets)

    return selected_tweet


def get_accs_to_monitor(monitor_accs_fname):
    with open(monitor_accs_fname) as csv_file:
        reader = csv.reader(csv_file)
        monitor_accs = [acc for acc in reader]
    return monitor_accs


def add_monitor_account(csv_fname, handle):
    """ Add Twitter handle to csv file"""
    handle = handle.removeprefix('@')
    with open(csv_fname) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(handle)


class TweetStream(tweepy.Stream):

    def on_data(self, data):
        print(data)

    def on_connection_error(self):  # Put error handling here
        self.disconnect()
