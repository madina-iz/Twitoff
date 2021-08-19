from twitoff3.twitter import add_or_update_user
from flask import Flask
from flask import render_template
from flask import request
from twitoff3.models import db, User
from twitoff3.predict import predict_user
import os

def create_app():
    
    app=Flask(__name__)
    
    # Setup database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

         
    @app.route("/reset")
    def reset():
        db.drop_all()
        db.create_all()
        return "database reset"

    @app.route("/", methods=["GET", "POST"])
    def home():
        name = request.form.get("name")

        if name:
            add_or_update_user(name)

        # To store a tweet for prediction
        # tweet = request.form.get("tweet")
                   
        users = User.query.all() or []
        return render_template("home.html", users=users)
                  

    @app.route("/compare", methods=["POST"])
    def compare():        
        user0, user1 = sorted(
            [request.values["user0"], request.values["user1"]])
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )
        return str(prediction)
        # return render_template("prediction.html", title="prediction", message=message)

    @app.route('/iris')
    def iris():    
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                    multi_class='multinomial').fit(X, y)
                            
        return str(clf.predict(X[:2, :]))
        
    return app
