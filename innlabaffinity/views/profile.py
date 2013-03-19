#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

from innlabaffinity import app, db
from innlabaffinity.decorators import *
from innlabaffinity.objects import User, get_user

from flask import render_template
from flask import url_for
from flask import session
from flask import abort
from flask import redirect
from flask import flash
import json

@app.route("/profile/<username>")
def show_profile(username):
    """Show user Profile"""
    profile = User()
    profile.database = db
    profile.username = username
    if not profile.already_exist():
        flash("Username not exists")
        redirect(url_for("homepage"))

    profile.load(username)
    return render_template("profile.html", profile=user)

@app.route("/profile/<username>/edit")
def edit_profile(username):
    """Edit Profile"""
    profile = get_user(session['user'], db)
    return render_template("edit_profile.html", profile=profile)


# API

@app.route("/api/profile/<username>")
def api_get_profile(username):
    """return Profile in json format"""
    return ""
    
@app.route("/api/profile/<username>/vote/new")
def api_vote_profile(username):
    """Vote Profile"""
    return ""
    
@app.route("/api/profile/<username>/vote")
def api_list_vote_profile(username):
    """Get votes Profile"""
    author = get_user(session['user'], db)
    user = get_user(username, db)
    
    if author.username not in user.vote_received:
        user.vote_received.append(author.username)
        user.save()
        
    return json.dumps({"status":"ok"})

@app.route("/api/profile/<username>/skills/set")
def api_set_skills_profile(username):
    """Set Skills Profile"""
    return ""
    
@app.route("/api/profile/<username>/interests/set")
def api_set_interests_profile(username):
    """Set interests Profile"""
    return ""
    
@app.route("/api/profile/<username>/description/set")
def api_set_description_profile(username):
    """Set Description Profile"""
    return ""