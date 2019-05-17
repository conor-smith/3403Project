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
    #backref p_user. Returns user object
    #backref p_gp. Returns GlobalPolls object
    
    #How to print this object
    def __repr__(self):
        return "<gp {}, user {}, score {}>".format(self.p_gp, self.p_user, self.score)

#An association ojbect. Is an object rather than a table because that makes it easier
#to record score/votes
class GlobalPolls(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey("poll.id"))          #id of poll
    m_id = db.Column(db.Integer, db.ForeignKey("media.id"))         #id of media
    parent_poll = db.relationship("Poll", backref = "associates")   #returns poll
    parent_med = db.relationship("Media", backref = "poll_votes")   #returns media
    all_votes = db.relationship("UserPolls", backref = "p_gp")      #returns all votes

    #How to print this object
    def __repr__(self):
        return "<poll {}, media {}>".format(self.parent_poll, self.parent_med)

#Stores all media
class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)                  #Name of media
    poster = db.Column(db.String(100), default = "img/poster.png")  #A string specifying a file in app/static/img
    mtype = db.Column(db.String(16), index = True)                  #Media type: Movie, Game, or Music
    #backref = poll. Returns all polls this is present in

    #How to print this object
    def __repr__(self):
        return "<Media {}>".format(self.title)

    #Deletes a particular peice of media
    def delete_media(self):
        db.session.delete(self)
        db.session.commit()

#Stores all polls
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))                                #The name of the poll(best sci-fi, etc)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))       #The id of the user who created the poll
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)   #The time and date of creation
    active = db.Column(db.Boolean(), default = True)                #Whether or not poll can be voted on
    mtype = db.Column(db.String(16), index = True, default = "All") #Movie, Game or Music
    choices = db.relationship("Media", secondary = "global_polls",  #Returns all media in this poll
                                backref = "poll")
    #backref = author. Returns creator of this poll
    #backref = associates. Returns all associated globalPolls objects

    #How to print this object
    def __repr__(self):
        return "<Poll {}>".format(self.name)

    #Check if poll contains media
    def contains(self, media):
        return media in self.choices

    #Add media to poll
    def add_media(self, media):
        if not self.contains(media):
            self.choices.append(media)
    
    #Remove media from poll(I don't know if this will be used but it's good to have)
    def remove_media(self, media):
        if self.contains(media):
            self.choices.remove(media)

    #Deletes poll
    def delete_poll(self):
        db.session.delete(self)
        db.session.commit()
    
    #Returns all participants
    def voters(self):
        vot = []
        for up in self.associates[0].all_votes:
            vot.append(up.p_user)
        return vot

    #Returns global totals for all choices
    def totals(self):
        tot = []
        for gp in self.associates:
            tally = 0
            for up in gp.all_votes:
                tally += up.score
            tot.append({"Media" : gp.parent_med, "GlobalScore" : tally})
        return tot

    #Returns one movie poster
    def cover(self):
        if len(self.choices) == 0:
            return "img/poster.png"
        return self.choices[0].poster

    #Deactivtes all current open polls
    def close_all():
        for p in Poll.query.filter(Poll.active).all():
            p.active = False
        
#Stores all users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)        
    username = db.Column(db.String(64), index = True, unique = True)#Username
    password_hash = db.Column(db.String(128))                       #Contains encrypted password
    admin = db.Column(db.Boolean(), default = False)                #if True, user is an admin
    created_polls = db.relationship("Poll", backref = "author",     #returns all polls created by this user
                                    lazy = "dynamic")
    votes = db.relationship("UserPolls", backref = "p_user")        #links to all votes of a user

    #How to print this object
    def __repr__(self):
        return "<User {}>".format(self.username)

    #Sets encrypted password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Checks password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Deletes account
    def delete_account(self):
        db.session.delete(self)
        db.session.commit()

    #checks if user has already participated in a poll
    def already_voted(self, poll):
        for up in self.votes:
            if up.p_gp.parent_poll == poll:
                return True
        return False

    #Removes previous votes(Used before redoing a poll)
    def remove_user_poll(self, poll):
        if self.already_voted(poll):
            for up in self.votes:
                if up.p_gp.parent_poll == poll:
                    db.session.delete(up)

    #Votes on a single entry in a single poll
    def vote_on_media(self, poll, media, score):
        for gp in poll.associates:
            if gp.m_id == media.id:
                db.session.add(UserPolls(u_id = self.id, gp_id = gp.id, score = score))
                break

    #Returns all polls the user has participated in
    def all_polls(self):
        ap = []
        for up in self.votes:
            if not up.p_gp.parent_poll in ap:
                ap.append(up.p_gp.parent_poll)
        return ap

    def poll_results(self, poll):
        pr = []
        for up in self.votes:
            if up.p_gp.parent_poll == poll:
                pr.append({"Media" : up.p_gp.parent_med , "Score" : up.score})
        return pr

@login.user_loader
def load_user(id):
    return User.query.get(int(id))