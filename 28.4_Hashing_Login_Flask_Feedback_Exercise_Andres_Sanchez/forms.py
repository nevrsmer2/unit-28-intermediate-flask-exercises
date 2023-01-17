from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(
        message='Required'), Length(max=20, message="20  characters max.")])

    password = PasswordField('Password', validators=[
                             InputRequired(), EqualTo('confirm', message='Passwords must match')])

    confirm = PasswordField('Confirm password')

    email = StringField("Email", validators=[InputRequired(
        message="Required Field"), Email(message="Invalid email format.")])

    first_name = StringField("First Name", validators=[
                             InputRequired(message="Required field.")])
    last_name = StringField("Last Name", validators=[
                            InputRequired(message="Required field.")])


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(
        message='Required'), Length(max=20, message="20  characters max.")])

    password = PasswordField("Password", validators=[
        InputRequired(message='Required')])


class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(
        message="Required."), Length(max=100, message="100 Characters Max.")])

    content = TextAreaField("Content", validators=[
        InputRequired(message="Required")])


class UpdateFeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(
        message="Required."), Length(max=100, message="100 Characters Max.")])

    content = TextAreaField("Content", validators=[
        InputRequired(message="Required")])


class DeleteForm(FlaskForm):
    """Delete form - delete user's instance of Feedback class"""
