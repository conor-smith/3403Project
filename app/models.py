from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.String(1), default = "F")
    created_polls = db.relationship("Poll", backref = "author", lazy = "dynamic")
    participated_polls = db.relationship("UserPoll", backref = "author", lazy = "dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)
    poster = db.Column(db.String(100), unique = True)
    mtype = db.Column(db.String(16), index = True)
    genre = db.Column(db.String(32), index = True)

    def __repr__(self):
        return "<Media {}>".format(self.title)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    genre = db.Column(db.String(32), index = True, default = "No Genre")
    mtype = db.Column(db.String(16), index = True, default = "All")
    choices = db.relationship("GlobalPolls", backref = "poll", lazy = "dynamic")
    
    def __repr__(self):
        return "<Poll {}>".format(self.name)

GlobalPolls = db.Table("globalpolls",
    db.Column("p_id", db.Integer, db.ForeignKey("poll.id")),
    db.Column("m_id", db.Integer, db.ForeignKey("media.id")),
    db.Column("score", db.Integer)
)

Userpolls = db.Table("userpolls",
    db.Column("p_id", db.Integer, db.ForeignKey("poll.id")),
    db.Column("u_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("m_id", db.Integer, db.ForeignKey("media.id")),
    db.Column("score", db.Integer)
)