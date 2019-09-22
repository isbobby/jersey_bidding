
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, InputRequired
from flask_login import current_user

class allocateForm(FlaskForm):
    yearToAllocate = SelectField('Year To Allocate', validators=[
                                 InputRequired()], coerce=int)
    submit = SubmitField('Go!')


class assignNumberForm(FlaskForm):
    assign = SelectField('Availible Numbers', validators=[
        DataRequired()], coerce=int)
    submit = SubmitField('Assign')

class chooseWaveForm(FlaskForm):
    waveToChoose = SelectField('Choose a wave', validators=[
                                 InputRequired()], coerce=int)
    submit = SubmitField('Go!')