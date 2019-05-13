from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')
@app.route('/front')
def front():
    user = current_user
    example_poll = {
        "img" : "img/poster.png"
    }
    polls = [example_poll, example_poll, example_poll, example_poll, example_poll, example_poll]
    return render_template("front.html", user=user, title="Front Page", polls=polls)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("front"))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first()
        if user is None or not user.check_password(lform.password.data):
            flash("Invalid username or password")
            return redirect(url_for("front"))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for("front"))
    return render_template("login.html", title="Log in", lform=lform)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("front"))