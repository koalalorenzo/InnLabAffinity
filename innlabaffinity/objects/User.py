#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

from hashlib import sha1
from datetime import datetime

class User(object):
    def __init__(self, username=None):
        self.username = username
        self.password = None
        self.__is_crypted = False
        
        self.first_name = ""
        self.second_name = ""
        self.email = ""
        self.avatar_url = "" # URL avatar

        self.group = "" # R1 || R2 || R3 || R4 || R5 || R6
        self.vote_received = list() # list of username

        self.description = ""
        self.skills = list()
        self.interests = list()
        self.looking_for_people = False
        
        self.blog_url = ""
        self.facebook_url = ""
        self.twitter_url = ""
        self.linkedin_url = ""
                
        self.keywords = list()
        
        self.database = None
        
    def change_password(self, new_password):
        if self.__is_crypted:
            self.password = sha1(new_password).hexdigest()
        else:
            self.password = new_password
        
    def __crypt_password(self):
        if not self.password: return
        if self.__is_crypted: return
        self.password = sha1(self.password).hexdigest()
        self.__is_crypted = True
        
    def already_exist(self):
        search = self.database.users.find_one({"username": self.username})
        if search:
            return True
        return False
        
    def verify_login(self, username, password):
        if self.__is_crypted:
            check = sha1(password).hexdigest()
        else: 
            check = password
        if self.password != check:
            return False
        return True

    def load(self, username):
        search = self.database.users.find_one({"username": self.username})
        if not search:
            raise Exception("Username not found")
        
        self.username = search['username']
        self.password = search['password']
        self.__is_crypted = True
        
        self.first_name = search['first_name']
        self.second_name = search['second_name']
        
        self.email = search['email']
        self.avatar_url = search['avatar_url']
        self.group = search['group']
        self.vote_received = search['vote_received']

        self.description = search['description']
        self.skills = search['skills']
        self.interests = search['interests']
        self.looking_for_people = search['looking_for_people']
        
        self.keywords = search['keywords']
 
        self.twitter_url = search['twitter_url']
        self.facebook_url = search['facebook_url']
        self.linkedin_url = search['linkedin_url']
        self.blog_url = search['blog_url']
        return
    
    def save(self):
        self.__crypt_password()
        search = self.database.users.find_one({"username": self.username})
        dictionary = self.__dict__(old=search)
        self.database.users.save(dictionary)

        return
        
    def __dict__(self, old=None):
        if not old:
            old = dict()
        
        old['username'] = self.username
        old['password'] = self.password
        
        old['first_name'] = self.first_name
        old['second_name'] = self.second_name
        
        old['email'] = self.email
        old['avatar_url'] = self.avatar_url
        old['group'] = self.group
        old['vote_received'] = self.vote_received
        
        old['description'] = self.description
        old['skills'] = self.skills
        old['interests'] = self.interests
        old['looking_for_people'] = self.looking_for_people
        
        old['keywords'] = self.keywords
 
        old['twitter_url'] = self.twitter_url
        old['facebook_url'] = self.facebook_url
        old['linkedin_url'] = self.linkedin_url
        old['blog_url'] = self.blog_url
        
        return old
        
def get_user(username, db):
    user = User(username)
    user.database = db
    try:
        user.load(username)
    except:
        return False
    if user.password:
        return user
    else:
        return False
