from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin

#An association table which links GlobalPolls to Users
class UserPolls(db.Model):
    #id of user
    u_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    #id of GlobalPolls object
    gp_id = db.Column(db.Integer, db.ForeignKey("global_polls.id"), primary_key = True)
    score = db.Column(db.Integer, default = 0)                      #Score given to this GP object by user
    parent_user = db.relationship("User", backref = "i_votes")
    parent_GP = db.relationship("GlobalPolls", backref = "all_votes")
    
    def __repr__(self):
        return "<gp {}, user {}>".format(self.parent_GP, self.parent_user)

#An association ojbect. Is an object rather than a table because that makes it easier
#to record score/votes
class GlobalPolls(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey("poll.id"))          #id of poll
    m_id = db.Column(db.Integer, db.ForeignKey("media.id"))         #id of media
    parent_poll = db.relationship("Poll", backref = "votes")        #returns poll
    parent_med = db.relationship("Media", backref = "poll_votes")   #returns media
    #backref = all_votes. Returns all UserPolls objects

    def __repr__(self):
        return "<poll {}, media {}>".format(self.parent_poll, self.parent_med)

#Stores all media
class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)                  #Name of media
    poster = db.Column(db.String(100), default = "img/poster.png")  #A sting specifying a file in app/static/img
    mtype = db.Column(db.String(16), index = True)                  #Movie, Game, or Music    
    #backref = poll. Returns all polls this is present in

    def __repr__(self):
        return "<Media {}>".format(self.title)

#Stores all polls
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))                                #The name of the poll(best sci-fi, etc)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))       #The id of the user who created the poll
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)   #The time and date of creation
    active = db.Column(db.String(1), default = "T")                 #Whether or not poll can be voted on
    mtype = db.Column(db.String(16), index = True, default = "All") #Movie, Game or Music
    choices = db.relationship("Media", secondary = "global_polls",  #Returns all media in this poll
                                backref = "poll")
    #backref = author. Returns creator of this poll
    #backref = votes. Returns all associated globalPolls objects

    def __repr__(self):
        return "<Poll {}>".format(self.name)

#Stores all users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)        
    username = db.Column(db.String(64), index = True, unique = True)#Username
    password_hash = db.Column(db.String(128))                       #Contains encrypted password
    admin = db.Column(db.String(1), default = "F")                  #if T, user is an admin
    created_polls = db.relationship("Poll", backref = "author",     #returns all polls created by this user
                                    lazy = "dynamic")
    voted = db.relationship("GlobalPolls", secondary = "user_polls",#Returns all GlobalPolls objects user has voted on
                            backref = "voters")
    #backref = i_votes. Returns all UserPolls objects

    #How to print this object
    def __repr__(self):
        return "<User {}>".format(self.username)

    #Sets encrypted password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Checks password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))