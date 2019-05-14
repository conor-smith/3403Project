from flask import render_template, redirect, url_for, flash, request
from app import app, db, admin
from app.forms import LoginForm, RegistrationForm, CreatePollForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Poll, Media
from flask_admin.contrib.sqla import ModelView

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("front"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in')
        if request.referrer is None:
            return redirect(url_for("front"))
        else:
            return redirect(request.referrer)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/create_polls', methods=['GET', 'POST'])
def create_polls():
    form = CreatePollForm()
    if form.validate_on_submit():
        flash("Poll creation success!")
        return redirect('/create_polls')
    return render_template("create_polls.html", form=form)

@app.route('/modify_admins')
def modify_admins():
    return render_template("modify_admins.html")

@app.route('/user_details')
def user_details():
    return render_template("user_details.html")

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login required")
        return redirect(url_for('login', next=request.url))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Poll, db.session))
admin.add_view(AdminView(Media, db.session))

# SUPER ADMIN/ADMIN #if id=1
# @app.route('/new_admin', methods=[POST]) # new account or upgrade user

# @app.route('/remove_user', methods=['DELETE']) # delete account entirely, do we need this?

# USER_DETAILS ROUTES
# @app.route('/change_user_password', methods=[PATCH]) # edit password of user

# user details
# @app.route('/change', methods=['DELETE']) # delete account entirely, do we need this?

# SHOW_POLLS ROUTES

# INDIVIDUAL POLL PAGES ROUTES

# POLL ARCHIVE ROUTES