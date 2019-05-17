from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
# https://github.com/wtforms/wtforms/blob/master/src/wtforms/fields/html5.py , it's undocumented on purpose apparently :shrug:
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from app.models import User, Poll


class VoteOnPoll(FlaskForm):

    submit = SubmitField("Vote!")

    #fields = ["vote{}".format(i+1) for i in range(10)]

    #choices = [(str(i+1),str(i+1)) for i in range(10)]
    
    vote1 = SelectField("vote1", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote2 = SelectField("vote2", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote3 = SelectField("vote3", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote4 = SelectField("vote4", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote5 = SelectField("vote5", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote6 = SelectField("vote6", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote7 = SelectField("vote7", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote8 = SelectField("vote8", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote9 = SelectField("vote9", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)
    vote10 = SelectField("vote10", choices=[(str(i+1),str(i+1)) for i in range(10)], default = 10)

    def get(self, field_name):
        getattr(self, field_name)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], 
        render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired()], 
        render_kw={"placeholder": "Password"})
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

# TODO email verification (optional)
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], 
        render_kw={"placeholder": "Username"})
    #email = EmailField("Email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField("Password", validators=[InputRequired()], 
        render_kw={"placeholder": "Password"})
    password2 = PasswordField("Repeat Password", validators=[InputRequired(), EqualTo('password')], 
        render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

# TODO complete other variables automatically e.g. creator, timestamp, etc.
# TODO validation checking for fields e.g. make sure name makes sense, or genre exists, etc.
class CreatePollForm(FlaskForm):
    #creator = 
    name = StringField("name", validators=[InputRequired()], 
        render_kw={"placeholder": "Name"})
    mtype = SelectField("Media Type", 
        choices=[("games", "Games"), ("movies", "Movies"), ("music", "Music")], 
        validators=[InputRequired()]) 
        # possible to add games, movie, music as only possible options in database instead of string type?
    #genre = SelectField("Genre", choices=[("horror", "Horror"), ("comedy", "Comedy"), ("drama", "Drama")], 
    #    validators=[InputRequired()]) 
        # PLACEHOLDER, probably need to make a set list of genres in database ahead of time,
        # and maybe superadmin ability to add new genres
        # also complicated with different media genres (e.g. RPG exists in games but not in movies and music)
    # choices = 
        # ???
    submit = SubmitField("Create Poll")

# TODO route for register, various admin page forms and various user forms
