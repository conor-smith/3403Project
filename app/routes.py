from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/front')
def front():
    example_user = {
        "username" : "Billtone",
        "isAdmin" : True
    }
    example_poll = {
        "img" : "img/poster.png"
    }
    polls = [example_poll, example_poll, example_poll, example_poll, example_poll, example_poll]
    return render_template("front.html", title="Front Page", current_user=example_user, polls=polls)
# I removed user=example_user to test log in functionality, current_user is part of user auth, incomplete
# should leave alone until I finish forms

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/create_polls')
def create_polls():
    return render_template("create_polls.html")

@app.route('/modify_admins')
def modify_admins():
    return render_template("modify_admins.html")

@app.route('/user_details')
def user_details():
    return render_template("user_details.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login success!")
        return redirect('/')
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Registration success!")
        return redirect('/')
    return render_template("register.html", form=form)

# TODO route for register, various admin page forms and various user forms