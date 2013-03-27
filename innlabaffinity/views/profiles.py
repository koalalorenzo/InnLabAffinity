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

@app.route("/profiles")
def show_profiles():
    """Show users Profiles"""
    profiles = db.users.find();
    return render_template("profiles.html",profiles=profiles)
   
@app.route("/profiles/group/",  methods=['POST'])
def show_profiles_in_group():
    """Show users Profiles"""
    profiles = db.users.find({'group': request.form['group'] })
    return render_template("profiles.html", profiles=profiles)
