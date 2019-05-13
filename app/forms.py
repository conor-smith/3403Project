from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# https://github.com/wtforms/wtforms/blob/master/src/wtforms/fields/html5.py , it's undocumented on purpose apparently :shrug:
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], 
        render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired()], 
        render_kw={"placeholder": "Password"})
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

# TODO email verification (optional)
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], 
        render_kw={"placeholder": "Username"})
    email = EmailField("Email", validators=[InputRequired(), Email()], 
        render_kw={"placeholder": "Email Address"})
    password = PasswordField("Password", validators=[InputRequired(), 
        EqualTo("confirm", message="Passwords must match")], render_kw={"placeholder": "Password"})
    confirm = PasswordField("Repeat Password", 
        render_kw={"placeholder": "Confirm Password"})
    prefGame = BooleanField("Prefers games")
    prefMovie = BooleanField("Prefers movies")
    prefMusic = BooleanField("Prefers music")
    submit = SubmitField("Register")


# TODO route for register, various admin page forms and various user forms