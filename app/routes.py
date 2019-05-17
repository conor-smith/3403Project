from flask import render_template, redirect, url_for, flash, request, Markup
from app import app, db, admin
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeUsernameForm
from flask_login import current_user, login_user, logout_user, login_required, CreatePollForm, VoteOnPoll
from app.models import User, Poll, Media
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from wtforms import PasswordField
from wtforms.validators import InputRequired, ValidationError, regexp
import os

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


@app.route('/manage_account')
@login_required
def manage_account():
    return render_template("manage_account.html", title="Manage Account", 
                            pwform=ChangePasswordForm(), unform=ChangeUsernameForm())


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    pwform = ChangePasswordForm()
    user = User.query.filter_by(username = current_user.username).first()
    if user is None or not user.check_password(pwform.current.data):
        flash("Current password is incorrect")
        return redirect(url_for("manage_account"))
    if pwform.validate_on_submit():
        user.set_password(pwform.new.data)
        db.session.add(user)
        db.session.commit()
        flash("Password change successful")
        return redirect(url_for("manage_account"))
    

@app.route('/change_username', methods=['POST'])
@login_required
def change_username():
    unform = ChangeUsernameForm()
    user = User.query.filter_by(username = unform.new.data).first()
    if not user is None:
        flash("Username already exists")
        return redirect(url_for("manage_account"))
    user = User.query.filter_by(username = current_user.username).first()
    if not user.check_password(unform.current.data):
        flash("Current password is incorrect")
        return redirect(url_for("manage_account"))
    if unform.validate_on_submit():
        user.username=unform.new.data
        db.session.commit()
        flash("Username change successful")
        return redirect(url_for("manage_account"))
    else:
        flash("error")
        return redirect(url_for("manage_account"))


# DATABASE DASHBOARD ROUTES
# TODO set all polls inactive
# TODO (low priority) edge case where only admin tries to un-admin themselves
# TODO (optional) show current unhashed password in users page
# TODO (optional) email
class UserView(ModelView):
    # All Views
    form_excluded_columns = ["password_hash"]
    form_extra_fields = {"change_pword": PasswordField("Set New Password")}

    # List View
    column_list = ["username", "admin", "votes"]
    column_exclude_list = ["password_hash"]
    column_filters = ["username", "admin"]

    # Create View
    form_create_rules = ["username", "change_pword", "admin"]

    # Edit View
    form_edit_rules = ["username", "change_pword", "admin",
                        "votes"]

    # Validation and and setting of database fields that are not automatic
    def on_model_change(self, form, model, is_created):
        if is_created:
            if not form.change_pword.data:
                raise ValidationError('Password Required')
        if not form.username.data:
            raise ValidationError('Username Required')
        # Sets password if there is input
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


class MediaView(ModelView):
    # All Views
    form_extra_fields = {
        "upload": ImageUploadField("Upload Poster Image", 
            base_path="app/static/img", max_size=[1400,2100, False], 
            allow_overwrite = False)
    }

    # List View
    column_list = ["title", "poster"]
    column_filters = ["title"]
    def get_poster_url(view, context, model, name):
        return Markup(
            u"<a href='%s'>%s</a>" % ("/static/" + model.poster,model.poster)
        ) if model.poster else u""
    column_formatters = dict(poster = get_poster_url)

    # Create View
    form_create_rules = ["title", "upload"]

    # Edit View
    form_edit_rules = ["title", "poll", "upload"]
    form_args = dict(poll=dict(label="Is In Polls"))
    form_widget_args = {"poll":{"disabled": True}}
    
    # Validation and setting of database fields that are not automatic
    def on_model_change(self, form, model, is_created):
        if not form.title.data:
            raise ValidationError('Title Required')
        # Sets filepath of poster image
        if form.upload.data:
            model.poster = "img/" + form.upload.data.filename

    # Delete poster image when deleting media from database if not the default image
    def on_model_delete(self, model):
        if not model.poster == "img/poster.png":
            if(os.path.isfile("app/static/" + model.poster)):
                os.remove("app/static/" + model.poster)

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


class PollView(ModelView):
    # List View
    column_list = ["name", "author", "timestamp"]
    column_filters = ["name", "author.username", "timestamp"]

    # Create View
    form_create_rules = ["name", "choices"]

    # Edit View
    form_edit_rules = ["name", "choices", "active", 
                        "timestamp", "author"]
    form_widget_args = {
        "timestamp" : {"disabled": True},
        "author" : {"disabled" : True}
        }

    # Validation and setting of database fields that are not automatic
    def on_model_change(self, form, model, is_created):
        if not form.name.data:
            raise ValidationError('Name Required')
        if not form.choices.data:
            raise ValidationError('Choices Required')
        # Sets author to user logged in at time
        model.author = current_user

    def on_model_delete(self, model):
        model.choices = []
    
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

# Adds a view for each database model
admin.add_view(UserView(User, db.session))
admin.add_view(MediaView(Media, db.session))
admin.add_view(PollView(Poll, db.session))