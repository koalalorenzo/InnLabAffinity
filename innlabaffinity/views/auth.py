from innlabaffinity import app, db
from innlabaffinity.decorators import *

from flask import render_template
from flask import url_for
from flask import session
from flask import abort
from flask import redirect
from flask import flash

from opinionbag.objects import User, get_user
import datetime

@app.route("/user/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for("homepage"))
    
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username)
        user.database = db
        try:
            user.load(username)
        except:
            flash(u"Invalid Username or Password", "error")
            return render_template('auth/login.html')
            
        if user.verify_login(username, password):
            flash(u"Welcome back %s %s" % (user.first_name, user.second_name), "info" )
            session['user'] = username
        else:
            flash(u"Invalid Username or Password", "error")
            return render_template('auth/login.html')
        return render_template('auth/login.html')

    return render_template('auth/login.html')

@app.route("/user/new", methods=['GET', 'POST'])
@app.route("/user/edit", methods=['GET', 'POST'])
def profile():
    the_user = None
    old_user = None
    already_registered = False
    username_editable = True
    
    if 'user' in session:
        already_registered = True
        old_user = get_user(session['user'], db)
        the_user = old_user
        if old_user:
            username_editable = False
        
    if request.method == 'POST':
        error = False
        username = request.form['username']
        
        if not old_user:
            the_user = User(username)
            the_user.database = db
            the_user.username = username
            username_editable = True
    
            the_user.registration_date = datetime.datetime.now()
            if the_user.already_exist():
                flash(u"Username already taken", "error")
                error = True
        else:
            the_user = old_user
            
        the_user.first_name = request.form['first_name']
        the_user.second_name = request.form['second_name']

        if len(request.form['email']) >= 9 and "@" in request.form['email']:
            the_user.email = request.form['email']
        else:
            flash(u"Insert a valid password", "error")
            error = True

        if request.form.has_key("blog_url"):
            if request.form['blog_url']:
                the_user.blog_url = request.form['blog_url']

        if request.form.has_key("twitter_url"):
            if request.form['twitter_url']:
                the_user.twitter_url = request.form['twitter_url']

        if request.form.has_key("facebook_url"):
            if request.form['facebook_url']:
                the_user.facebook_url = request.form['facebook_url']

        if request.form.has_key("linkedin_url"):
            if request.form['linkedin_url']:
                the_user.linkedin_url = request.form['linkedin_url']

        if request.form.has_key("avatar_url"):
            if request.form['avatar_url']:
                the_user.avatar_url = request.form['avatar_url']

        the_user.type = int(request.form['type'])

        if request.form.has_key("password"):
            if len(request.form['password']) >= 6:
                the_user.change_password(request.form['password'])
            elif len(request.form['password']) == 0 and not username_editable:
                pass
            else:
                flash(u"The password must have more than 5 characters", "error")
                error = True
                
        if error:
            return render_template('auth/profile.html', user=old_user, puser=the_user, page="profile", username_editable=username_editable)
        
        the_user.save()
        if already_registered:
            flash(u"Profile updated", "success")
        else:
            flash(u"Registration complete! An email has sent to %s to verify your account." % the_user.email, "success")
            return redirect(url_for('homepage'))
            
        return render_template('auth/profile.html', user=old_user, puser=the_user, page="profile", username_editable=username_editable)

    return render_template('auth/profile.html', user=old_user, puser=the_user, page="profile", username_editable=username_editable)
        
@app.route("/user/logout")
def logout():
    session.pop('user', None)
    flash("Goodbye!", "info")    
    return redirect(url_for('homepage'))