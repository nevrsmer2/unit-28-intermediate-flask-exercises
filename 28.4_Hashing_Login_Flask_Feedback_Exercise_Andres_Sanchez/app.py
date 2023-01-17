from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from forms import (DeleteForm, FeedbackForm, LoginForm, RegisterForm,
                   UpdateFeedbackForm)
from models import Feedback, User, connect_db, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "I_l0v3-ki7713S"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


'''-------------------------USER ROUTES-------------------------'''


@app.route('/')
def root():
    '''Redirect to page to register.'''
    return redirect('/users/register')


@app.route('/users/register', methods=["GET", "POST"])
def render_register_form():
    '''Render form to register user and handle create new user functionality'''

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('users/register.html', form=form)

        session['username'] = new_user.username
        return redirect(f"/users/{new_user.username}")

    return render_template('users/register.html', form=form)


@app.route("/users/login", methods=["GET", "POST"])
def render_login_form():
    '''Render the login form and handle user authentication'''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template("users/login.html", form=form)


@app.route('/users/<username>')
def user_details(username):
    """Show a page with info on a specific user"""
    form = DeleteForm()
    user = User.query.get(username)

    if "username" not in session or username != session['username']:
        # flash("Please login first!", "danger")
        return redirect('/users/login')

    return render_template('users/info.html', user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    '''Delete the signed in user'''

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/users/login")


'''-------------------------FEEDBACK ROUTES-------------------------'''


@app.route("/feedback/<username>/add", methods=["GET", "POST"])
def render_add_feedback_form(username):
    '''Render form to add feedback'''

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback/add.html", form=form)


@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def update_feedback(id):
    '''Render form to update current user's feedback'''

    feedback = Feedback.query.get_or_404(id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = UpdateFeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/update.html", form=form, feedback=feedback)


@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):
    '''Delete logged in user's feedback.'''

    feedback = Feedback.query.get_or_404(id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")


@app.route('/logout')
def logout_user():
    '''Log current user out.'''
    session.pop('username')
    return redirect('/users/login')
