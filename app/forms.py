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

# TODO email (optional)
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

class ChangePasswordForm(FlaskForm):
    current = PasswordField("Current Password", validators=[InputRequired()], 
        render_kw={"placeholder": "Current Password"})
    new = PasswordField("New Password", validators=[InputRequired()], 
        render_kw={"placeholder": "New Password"})
    confirm = PasswordField("Confirm New Password", validators=[InputRequired(), EqualTo('new')],
        render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField("Change Password")

class ChangeUsernameForm(FlaskForm):
    current = PasswordField("Current Password", validators=[InputRequired()], 
        render_kw={"placeholder": "Current Password"})
    new = PasswordField("New Username", validators=[InputRequired()], 
        render_kw={"placeholder": "New Username"})
    submit = SubmitField("Change Username")