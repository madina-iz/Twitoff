from flask import Flask
from flask import render_template
from flask import request
from .models import db, User
import os


def create_app():
    # get path to the pp directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Location of the database in the app directory
    database = "sqlite:///{}".format(os.path.join(app_dir, "twitoff.sqlite3"))
    
    app = Flask(__name__)
    
    # Setup database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    
    @app.route("/", methods=["GET", "POST"])
    def home():
        name = request.form.get("name")
        
        if name:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            
        users = User.query.all()
        return render_template("home.html", users=users)
        
    return app