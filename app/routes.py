from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/front')
def front():
    example_poll = {
        "img" : "img/poster.png"
    }
    polls = [example_poll, example_poll, example_poll, example_poll, example_poll, example_poll]
    return render_template("front.html", title="Front Page", polls=polls)

@app.route('/login')
def login():
    lform = LoginForm()
    return render_template("login.html", title="Log in", lform=lform)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")