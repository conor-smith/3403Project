from flask import render_template, redirect, url_for, flash, request, Markup, abort
from app import app, db, admin
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeUsernameForm, VoteOnPoll
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Poll, Media, GlobalPolls, UserPolls
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin.actions import action
from wtforms import PasswordField
from wtforms.validators import InputRequired, ValidationError, regexp
import os
import warnings

@app.route('/')
@app.route('/front')
def front():
    polls = Poll.query.filter(Poll.active).all()
    return render_template("front.html", title="Front Page", polls=polls)

@app.route('/archives')
@login_required
def archives():
    active = Poll.query.filter(Poll.active).all()
    inactive = Poll.query.filter(Poll.active == False).all()
    return render_template("archives.html", title="Archives", active=active, inactive=inactive)

@app.route('/poll/<id>', methods=['GET', 'POST'])
def poll_page(id):
    poll = Poll.query.get(int(id))
    if current_user.is_anonymous or not poll.active:
        return redirect(url_for("poll_results", id=id))
    vform = VoteOnPoll()
    if vform.validate_on_submit():
        current_user.remove_user_poll(poll)
        for i in range(len(poll.choices)):
            data = int(getattr(vform, "vote{}".format(i+1)).data)
            if data < 1 or data > len(poll.choices):
                data = len(poll.choices)
            current_user.vote_on_media(poll, poll.choices[i], data)
        db.session.commit()
        return redirect(url_for("poll_results", id=id))
    if not poll:
        abort(404)
    length = len(poll.choices)
    fields = ["vote{}".format(i+1) for i in range(10)]
    return render_template("poll_page.html", extra_js="javascript/voting.js", title=poll.name, poll=poll,
        extra_css="css/voting.css", length=length, vform=vform, fields=fields)

@app.route('/poll/results/<id>')
def poll_results(id):
    poll = Poll.query.get(int(id))
    if not poll:
        abort(404)
    sorted_scores = sorted(poll.totals(), key = lambda i: i["GlobalScore"])
    if current_user.is_authenticated:
        for ss in sorted_scores:
            for us in current_user.poll_results(poll):
                if us["Media"] == ss["Media"]:
                    ss["UserScore"] = us["Score"]
    return render_template("poll_results.html", title=poll.name+" results", poll=poll, data=sorted_scores, length=len(sorted_scores))

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
# TODO add ability to delete individual responses (by poll instead of individually)
# TODO (low priority) edge case where only admin tries to un-admin themselves
# TODO (optional) show current unhashed password in users page
# TODO (optional) email
class UserView(ModelView):
    edit_template = "admin/edit.html"
    # All Views
    form_excluded_columns = ["password_hash"]
    form_extra_fields = {"change_pword" : PasswordField("Set New Password")}

    # List View
    column_list = ["username", "admin", "allpolls"]
    column_exclude_list = ["password_hash"]
    column_filters = ["username", "admin"]
    column_labels = dict(allpolls="Polls")
    def get_polls(view, context, model, name):
        if model.all_polls:
            polls = model.all_polls()
            label = ""
            count = 0
            for p in polls:
                if count == 0:
                    label = label + p.name
                    count = 1
                else:
                    label =  label + ", " + p.name
            return Markup(u"%s" % (label))
        else:
            return u""
    column_formatters = dict(allpolls = get_polls)

    # Create View
    form_create_rules = ["username", "change_pword", "admin"]

    # Edit View
    form_edit_rules = ["username", "change_pword", "admin", "votes"]

    # Deletes all responses that a user has submitted
    @action('delresponse', 'Delete All Response(s)', 'Are you sure you want delete these response(s)?')
    def action_delresponse(self, ids):
        for _id in ids:
            user = User.query.get(int(_id))
            poll = user.all_polls()
            for p in poll:
                user.remove_user_poll(p)
            db.session.commit()
        flash("{}'s response(s) deleted".format(user.username))
    
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

    # Deletes user responses before deleting a user
    def on_model_delete(self, model):
        poll = model.all_polls()
        for p in poll:
            model.remove_user_poll(p)
        db.session.commit()
    
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
        # If poster is changed, delete old poster
        if not is_created:
            if(not "img/" + form.upload.data.filename == model.poster):
                os.remove("app/static/" + model.poster)
        # Sets filepath of poster image
        if form.upload.data:
            model.poster = "img/" + form.upload.data.filename


    # Delete poster image when deleting media from database if not the default image
    # Also deletes related association objects
    def on_model_delete(self, model):
        if not model.poster == "img/poster.png":
            if(os.path.isfile("app/static/" + model.poster)):
                os.remove("app/static/" + model.poster)

        assoc2 = GlobalPolls.query.filter(GlobalPolls.m_id == model.id).all()
        for gp in assoc2:
            assoc1 = UserPolls.query.filter(UserPolls.gp_id == gp.id).all()
            for up in assoc1:
                db.session.delete(up)
                db.session.commit()
            db.session.delete(gp)
            db.session.commit()

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

# TODO fix bug where deleting media from a poll leaves behind associaton objects where it used to exist
class PollView(ModelView):
    # List View
    column_list = ["name", "author", "timestamp", "keyword"]
    column_filters = ["name", "author.username", "timestamp", "keyword"]

    # Create View
    form_create_rules = ["name", "choices", "keyword"]

    # Edit View
    form_edit_rules = ["name", "choices", "active", 
                        "timestamp", "author", "keyword"]
    form_widget_args = {
        "timestamp" : {"disabled": True},
        "author" : {"disabled" : True}
        }

    @action('inactive', 'Set Inactive', 'Are you sure you want to set these poll(s) as inactive?')
    def action_active(self, ids):
        count = 0
        for _id in ids:
            poll = Poll.query.get(int(_id))
            poll.active = False
            db.session.commit()
            count += 1
        flash("{0} poll(s) set inactive".format(count))
    
    # Validation and setting of database fields that are not automatic
    def on_model_change(self, form, model, is_created):
        if not form.name.data:
            raise ValidationError('Name Required')
        if not form.choices.data:
            raise ValidationError('Choices Required')
        if not form.keyword.data:
            raise ValidationError('Keyword Required')
        # Sets author to user logged in at time
        if is_created:
            model.author = current_user

    # Deletes user votes on the poll that is getting deleted and removes related assocations 
    def on_model_delete(self, model):
        for v in model.voters():
            v.remove_user_poll(model)
        db.session.commit()
        model.choices = []
        model.associates = []

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
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
    admin.add_view(UserView(User, db.session))
    admin.add_view(MediaView(Media, db.session))
    admin.add_view(PollView(Poll, db.session))
