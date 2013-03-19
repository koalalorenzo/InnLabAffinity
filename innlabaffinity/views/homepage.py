from innlabaffinity import app
from innlabaffinity.decorators import *

from flask import render_template

@app.route("/")
@cached()
def homepage():
    """Homepage"""
    return render_template("homepage.html")