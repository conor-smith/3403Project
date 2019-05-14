from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin

userpolls = db.Table("userpolls",
    db.Column("p_id", db.Integer, db.ForeignKey("poll.id")),
    db.Column("u_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("m_id", db.Integer, db.ForeignKey("media.id")),
    db.Column("score", db.Integer, default = 0)
)

globalpolls = db.Table("globalpolls",
    db.Column("p_id", db.Integer, db.ForeignKey("poll.id")),
    db.Column("m_id", db.Integer, db.ForeignKey("media.id")),
    db.Column("score", db.Integer)
)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True)
    poster = db.Column(db.String(100), default = "img/poster.png")
    mtype = db.Column(db.String(16), index = True)

    def __repr__(self):
        return "<Media {}>".format(self.title)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    active = db.Column(db.String(1), default = "T")
    mtype = db.Column(db.String(16), index = True, default = "All")
    choices = db.relationship(
        "Media", secondary = globalpolls,
        primaryjoin = (globalpolls.c.p_id == id),
        secondaryjoin = (globalpolls.c.m_id == Media.id),
        backref = db.backref("polls", lazy = "dynamic"), lazy = "dynamic"
    )
    
    def __repr__(self):
        return "<Poll {}>".format(self.name)
    
    def contains(self, media):
        return self.choices.filter(globalpolls.c.m_id == media.id).count() > 0

    def add_media(self, media):
        if not self.contains(media):
            self.choices.append(media)
    
    def remove_media(self, media):
        if self.contains(media):
            self.choices.remove(media)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean(1), default = False)
    created_polls = db.relationship("Poll", backref = "author", lazy = "dynamic")
    participated = db.relationship(
        "Poll", secondary = userpolls,
        primaryjoin = (userpolls.c.u_id == id),
        secondaryjoin = (userpolls.c.p_id == Poll.id),
        backref = db.backref("participants", lazy = "dynamic"), lazy = "dynamic"
    )

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))