from os import getenv
from twitoff3.models import db, Tweet, User
import tweepy
import spacy


# Authenticates us and allows us to use the Twitter API
TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(TWITTER_AUTH)

# Load nlp model
nlp = spacy.load('my_nlp_model')

# Vectorize tweets
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    
    twitter_user = api.get_user(username)
    
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, name=username)
    db.session.add(db_user)
    
    tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended")
    #         since_id=db_user.newest_tweet_id
    #     )
        
    # if tweets:
    #     db_user.newest_tweet_id = tweets[0].id
        
    for tweet in tweets:
        vecs = vectorize_tweet(tweet.full_text)
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vector=vecs)
        db_user.tweets.append(db_tweet)
        db.session.add(db_tweet)
        
    db.session.commit()
