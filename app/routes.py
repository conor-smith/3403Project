from flask import render_template
from app import app

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
    return render_template("front.html", title="Front Page", user=example_user, polls=polls)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")