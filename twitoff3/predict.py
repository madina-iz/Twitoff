import numpy as np
from sklearn.linear_model import LogisticRegression
import tweepy
import spacy
import en_core_web_sm
import pickle

TWITTER_API_KEY = "RhLwEal1HaKFO96oXiYjHDlC6"
TWITTER_API_KEY_SECRET = "4BLMVQbNnJ3PDB4518MW2Z772b7TBBPlUeXcS8KBdYFqKIg2c9"

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)

twitter = tweepy.API(auth)

nasa = twitter.get_user("nasa")
jeff = twitter.get_user("jeffbezos")

nasa_tweets = nasa.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")

jeff_tweets = jeff.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")

nlp_model = en_core_web_sm.load()


"""Prediction of Users based on Tweet embeddings."""

# Package imports
import numpy as np
import spacy
from sklearn.linear_model import LogisticRegression

# Local imports
from twitoff3.models import User


def predict_user(user1_name, user2_name, tweet_text):
    """Determine and returns which user is more likely to say a given Tweet."""
    # SELECT name FROM User WHERE name = <user1_name> LIMIT 1;
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    # Embed the tweets using Basilica's functionality
    user1_embeddings = np.array([tweet.vector for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.vector for tweet in user2.tweets])

    # X = embeddings
    # y = labels
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.zeros(len(user1.tweets)),
                             np.ones(len(user2.tweets))])

    # Fit a LogisticRegression model on X and y
    log_reg = LogisticRegression().fit(embeddings, labels)

    # Embed the tweet_text using SpaCy vectorizer to use with predictive model
    nlp = spacy.load('twitoff3/my_nlp_model')
    tweet_embedding = nlp(tweet_text).vector

    # Return the predicted label
    # [0.] = user1  //  [1.] = user2
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
