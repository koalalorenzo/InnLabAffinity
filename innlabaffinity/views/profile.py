from innlabaffinity import app
from innlabaffinity.decorators import *
from innlabaffinity.objects import User, get_user

from flask import render_template

@app.route("/profile/<username>")
@cached()
def show_profile(username):
    """Show user Profile"""
    
    return render_template("homepage.html")
    
@app.route("/profile/<username>/edit")
@cached()
def edit_profile(username):
    """Edit Profile"""
    
    
    return render_template("homepage.html")