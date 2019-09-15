
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user

class allocateForm(FlaskForm):
    yearToAllocate = SelectField('Year To Allocate', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Allocate!')
