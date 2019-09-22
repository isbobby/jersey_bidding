
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user


class chopeNumberForm(FlaskForm):
    submit = SubmitField('I want this number')


class biddingFormSenior(FlaskForm):
    firstChoice = SelectField('First Choice', validators=[
                              DataRequired()], coerce=int)
    secondChoice = SelectField('Second Choice', validators=[
                               DataRequired()], coerce=int)
    thirdChoice = SelectField('Third Choice', validators=[
                              DataRequired()], coerce=int)
    fourthChoice = SelectField('Fourth Choice', validators=[
                               DataRequired()], coerce=int)
    fifthChoice = SelectField('Fifth Choice', validators=[
                              DataRequired()], coerce=int)
    wantUniqueNumber = SelectField('I want my number to be unique.',  coerce=int)
    submit = SubmitField('Submit my choices')

class biddingFormJunior(FlaskForm):
    firstChoice = SelectField('First Choice', validators=[
                              DataRequired()], coerce=int)
    secondChoice = SelectField('Second Choice', validators=[
                               DataRequired()], coerce=int)
    thirdChoice = SelectField('Third Choice', validators=[
                              DataRequired()], coerce=int)
    fourthChoice = SelectField('Fourth Choice', validators=[
                               DataRequired()], coerce=int)
    fifthChoice = SelectField('Fifth Choice', validators=[
                              DataRequired()], coerce=int)
    submit = SubmitField('Submit my choices')

class allocateForm(FlaskForm):
    yearToAllocate = SelectField('Year To Allocate', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Allocate!')
