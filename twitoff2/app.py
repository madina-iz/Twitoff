from flask import Flask
from flask import render_template
from flask import request
from .models import db, User, Tweet
import os
import tweepy
import spacy
import en_core_web_sm


# Connect to twitter
TWITTER_API_KEY = "RhLwEal1HaKFO96oXiYjHDlC6"
TWITTER_API_KEY_SECRET = "4BLMVQbNnJ3PDB4518MW2Z772b7TBBPlUeXcS8KBdYFqKIg2c9"


def create_app():
    # get path to the pp directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Location of the database in the app directory
    database = "sqlite:///{}".format(os.path.join(app_dir, "twitoff.sqlite3"))
    
    app = Flask(__name__)
    
    # Setup database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    twitter = tweepy.API(auth)

    # Load saved nlp model
    nlp_model = spacy.load('my_nlp_model')

    
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.drop_all()
        db.create_all()
        
    
    @app.route("/", methods=["GET", "POST"])
    def home():

        name = request.form.get("name")      
        if name:
            # user = User(name=name)
            t_user = twitter.get_user(name)
            t_user_tweets = t_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")
            t_tweet = t_user_tweets[0].text
            # tweet_vec = nlp_model(t_tweet).vector
            t_user_id = int(t_user.id_str)
            user = User(id=t_user_id, name=name)
            tweet = Tweet(id=t_user_tweets[0].id, tweet=t_tweet,
                          user_id=user.id)
            
            db.session.add(user)
            db.session.add(tweet)
            db.session.commit()

        
            
        users = User.query.all()
        return render_template("home.html", users=users)
        
    return app
