import tweepy
import os
from dotenv import load_dotenv
from random import choice
import schedule
import time
load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)


def select_random_file():
    return choice(os.listdir("images"))


def media_upload(file_path):
    media = api.media_upload(file_path)
    return media.media_id


def send_dm(user_id, file_path):
    media_id = media_upload(file_path)
    message = "This is an image"
    api.send_direct_message(recipient_id=user_id, text=message,
                            attachment_type="media", attachment_media_id=media_id)


def send_tweet(file_path):
    media_id = media_upload(file_path)
    message = "This is a test ducky, sent via bot"
    api.update_status(message, attachment_media_ids=[media_id])


x = os.getenv("USER_NAME")
user_id = api.get_user(screen_name=x).id


def main():
    file_path = './images/'+select_random_file()
    send_dm(user_id, file_path)


main()
schedule.every(1).hours.do(main)
while True:
    try:
        schedule.run_pending()
        time.sleep(0)
    except:
        exit()
