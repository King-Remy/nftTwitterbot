# Import our libraries
from tkinter import Frame
import pandas as pd
import tweepy
import re
from dotenv import load_dotenv
import os
import yaml
import datetime

# Define the keys
load_dotenv('.env')
consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
Bearer_token = os.getenv('BEARER_TOKEN')

# define authentication handler
auth_handler = tweepy.OAuth1UserHandler(consumer_key,consumer_secret)

# Set access tokens
auth_handler.set_access_token(access_token,access_token_secret)

# Creating the API
api = tweepy.API(auth_handler,wait_on_rate_limit=True)

# Creating client token
client = tweepy.Client(bearer_token=Bearer_token)

# Searching tweets
search_term='NFTshill NFTs NFTdrop -filter:retweets'
tweet_amount=1000
# Create a cursor object
tweets=tweepy.Cursor(api.search_tweets,q=search_term,lang='en',tweet_mode='extended').items(tweet_amount)

usernames = []
final_users = []
# u_followers = []
# u_description = []
u_top = []


with open("config.yaml","r") as file:
    top_accounts = yaml.safe_load(file)

users = client.get_users(usernames=top_accounts['accounts'])

top_user_id =  [user.id for user in users.data]

words = "|".join(top_accounts['words'])

for tweet in tweets: 
    screen_names = tweet.user.screen_name
    followers = tweet.user.followers_count
    desription = tweet.user.description
    created = tweet.user.created_at.date()

    if  followers < 20000 and re.findall(pattern = words,string = desription) and created.year == 2022 and created.month >= 5:
        fol = tweet.user.follower_ids()
        top_user = set(top_user_id) & set(fol)
        u_top.append(top_user)
        final_users.append(screen_names)

        second = []
        for user in top_user_id:
            if user in fol:
                second.append(user)
        print(second)



# write each tweet as a row to a data Frame
# manually inspect the information
# make yaml list case sensitive
# .JOIN method in strings to join items in the list
# Switch to a stream for live data 
# Do a readme file for the project

print(u_top)
print(final_users)
print(second)

# d = {'Username': users,'Followers':u_followers,'Description':u_description}
# df = pd.DataFrame(d)

# df.head()

# print(df.head(10))