from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
# https://github.com/wtforms/wtforms/blob/master/src/wtforms/fields/html5.py , it's undocumented on purpose apparently :shrug:
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from app.models import User, Poll


class VoteOnPoll(FlaskForm):

    submit = SubmitField("Submit!")
    
    vote1 = StringField("vote1", default = 10)
    vote2 = StringField("vote2", default = 10)
    vote3 = StringField("vote3", default = 10)
    vote4 = StringField("vote4", default = 10)
    vote5 = StringField("vote5", default = 10)
    vote6 = StringField("vote6", default = 10)
    vote7 = StringField("vote7", default = 10)
    vote8 = StringField("vote8", default = 10)
    vote9 = StringField("vote9", default = 10)
    vote10 =StringField("vote10", default = 10)

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