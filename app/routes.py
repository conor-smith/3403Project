from flask import render_template, redirect, url_for, flash, request
from app import app, db, admin
from app.forms import LoginForm, RegistrationForm, CreatePollForm, VoteOnPoll
from flask_login import current_user, login_user, logout_user
from app.models import User, Poll, Media
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField
from wtforms.validators import InputRequired, ValidationError

@app.route('/')
@app.route('/front')
def front():
    polls = Poll.query.filter(Poll.active).all()
    return render_template("front.html", title="Front Page", polls=polls)

@app.route('/poll/<id>', methods=['GET', 'POST'])
def poll_page(id):
    if current_user.is_anonymous:
        return redirect(url_for("poll_results", id=id))
    poll = Poll.query.get(int(id))
    vform = VoteOnPoll()
    if vform.validate_on_submit():
        current_user.remove_user_poll(poll)
        for i in range(len(poll.choices)):
            current_user.vote_on_media(poll, poll.choices[i], int(getattr(vform, "vote{}".format(i+1)).data))
        db.session.commit()
        return redirect(url_for("front"))
    length = len(poll.choices)
    fields = ["vote{}".format(i+1) for i in range(10)]
    if vform.validate_on_submit():
        return redirect(url_for("front"))
    return render_template("poll_page.html", title=poll.name, poll=poll, length=length, vform=vform, fields=fields)

@app.route('/poll/results/<id>')
def poll_results(id):
    poll = Poll.query.get(int(id))
    sorted_scores = sorted(poll.totals(), key = lambda i: i["GlobalScore"])
    if current_user.is_authenticated:
        for ss in sorted_scores:
            for us in current_user.poll_results(poll):
                if us["Media"] == ss["Media"]:
                    ss["UserScore"] = us["Score"]
    return render_template("poll_results.html", data=sorted_scores, length=len(sorted_scores))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("front"))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first_or_404()
        if user is None or not user.check_password(lform.password.data):
            flash("Invalid username or password")
            return redirect(url_for("front"))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for("front"))
    return render_template("login.html", title="Log in", lform=lform)

@app.route('/logout')
def logout(): 
    logout_user()
    flash("You have logged out successfully")
    return redirect(url_for("front"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in")
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
        flash("Thanks for registering, please log in")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route('/about_us')
def about_us():
    return render_template("about_us.html", title="About Us")

# SHOW_POLLS ROUTES

# INDIVIDUAL POLL PAGES ROUTES

# POLL ARCHIVE ROUTES

# MANAGE ACCOUNT ROUTES (where user can change their own details like email or password)
# edit password, edit username (optional), edit email (optional), 

# DATABASE DASHBOARD ROUTES
# This section covers adding and removing both normal and admin accounts, 
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            flash("Admin access required")
            if request.referrer is None:
                return redirect(url_for("front"))
            else:
                return redirect(request.referrer)
        else:
            flash("Login required")
            return redirect(url_for("login", next=request.url))

# TODO what fields are mandatory in poll
# TODO what fields are mandatory in media
# TODO (optional) show current unhashed password in users page
class UserView(ModelView):
    form_create_rules = ["username", "change_pword", "admin"]
    form_edit_rules = ["username", "change_pword", "admin",
        "votes", "created_polls"]
    form_excluded_columns = ["password_hash"]
    form_extra_fields = {
        "change_pword": PasswordField("Set New Password")
    }
    
    # Validation and setting new password if there is input
    def on_model_change(self, form, model, is_created):
        if is_created:
            if not form.username.data:
                raise ValidationError('Username Required')
            if not form.change_pword.data:
                raise ValidationError('Password Required')
        
        if form.change_pword.data:
            model.set_password(form.change_pword.data)

    # Check if logged in and is admin when accessing admin pages
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    # What to do if not logged in/not admin
    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            flash("Admin access required")
            if request.referrer is None:
                return redirect(url_for("front"))
            else:
                return redirect(request.referrer)
        else:
            flash("Login required")
            return redirect(url_for("login", next=request.url))

# Adds a page for each database model
admin.add_view(UserView(User, db.session))
admin.add_view(AdminView(Poll, db.session))
admin.add_view(AdminView(Media, db.session))