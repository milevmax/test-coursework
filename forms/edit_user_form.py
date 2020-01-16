from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class UserEditForm(FlaskForm):

    user_name = StringField('name', validators=[DataRequired(), Length(2)])

    user_age = IntegerField('age', validators=[DataRequired(), NumberRange(min=18, max=100)])

    skin_condition = IntegerField('skin', validators=[DataRequired(), NumberRange(min=1, max=10)])

    submit = SubmitField("Save")