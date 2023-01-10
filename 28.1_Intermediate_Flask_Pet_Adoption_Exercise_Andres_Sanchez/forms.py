from flask_wtf import FlaskForm
from wtforms import (BooleanField, FloatField, IntegerField, StringField,
                     TextAreaField)
from wtforms.validators import (URL, AnyOf, Email, InputRequired, NumberRange,
                                Optional)

permitted_pets = ['cat', 'dog',  'porcupine']


class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[
                       InputRequired(message='Pet name is required')])

    species = StringField('Species', validators=[
        InputRequired(message='Species is required'), AnyOf(permitted_pets, message='Only cats, dogs and porcupines', values_formatter=None)])

    age = IntegerField('Age', validators=[Optional(), NumberRange(
        min=0, max=30, message='Age must be between 0-30')])

    photo_url = StringField('Photo URL', validators=[Optional(), URL(
        require_tld=True, message='Must be a valid URL.')])

    notes = TextAreaField('Notes')


class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators=[Optional(), URL(
        require_tld=True, message='Must be a valid URL.')])

    notes = TextAreaField('Notes')

    # available = BooleanField(
    #     validators=[InputRequired(message='Enter True or False.')])

    available = BooleanField("Available?")

    # available = BooleanField(default field arguments, false_values=None)
    # https://code.luasoftware.com/tutorials/python/wtforms-booleanfield-value-and-validation
