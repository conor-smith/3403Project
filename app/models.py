from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin


class UserPolls(db.Model):
    u_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    gp_id = db.Column(db.Integer, db.ForeignKey("global_polls.id"), primary_key = True)
    score = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return "<gp {}, user {}>".format(self.gp_id, self.u_id)

class GlobalPolls(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    p_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    m_id = db.Column(db.Integer, db.ForeignKey("media.id"))
    score = db.Column(db.Integer, default = 0)
    parent_poll = db.relationship("Poll", backref = "votes")
    parent_med = db.relationship("Media", backref = "poll_votes")

    def __repr__(self):
        return "<poll {}, media {}>".format(self.parent_poll, self.parent_med)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)
    poster = db.Column(db.String(100), default = "img/poster.png")
    mtype = db.Column(db.String(16), index = True)
    polls = db.relationship("Poll", secondary = "global_polls")

    def __repr__(self):
        return "<Media {}>".format(self.title)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    active = db.Column(db.String(1), default = "T")
    mtype = db.Column(db.String(16), index = True, default = "All")
    choices = db.relationship("Media", secondary = "global_polls")
    
    def __repr__(self):
        return "<Poll {}>".format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.String(1), default = "F")
    created_polls = db.relationship("Poll", backref = "author", lazy = "dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))