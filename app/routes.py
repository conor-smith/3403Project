from flask import render_template
from app import app

@app.route('/')
def front_page():
    example_user = {
        "username" : "Billtone",
        "isAdmin" : True
    }
    example_poll = {
        "img" : "img/poster.png"
    }
    polls = [example_poll, example_poll, example_poll, example_poll, example_poll, example_poll]
    return render_template("Front.html", title="Front page", user=example_user, polls=polls)