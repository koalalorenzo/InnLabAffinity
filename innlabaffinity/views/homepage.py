from innlabaffinity import app
from innlabaffinity.decorators import *
from innlabaffinity.objects import User, get_user

from flask import render_template
from flask import session

@app.route("/")
def homepage():
    """Homepage"""
    user = None
    if session.has_key('user'):
        user = get_user(session['user'], db)
    
    return render_template("homepage.html", user=user)