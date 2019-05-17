from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
# https://github.com/wtforms/wtforms/blob/master/src/wtforms/fields/html5.py , it's undocumented on purpose apparently :shrug:
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, ValidationError
from app.models import User

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
