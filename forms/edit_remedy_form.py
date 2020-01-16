from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class EditRemedyForm(FlaskForm):

    remedy_name = StringField('name', validators=[DataRequired(), Length(3)])

    remedy_color = StringField('color', validators=[DataRequired(), Length(2)])

    remedy_brightness = StringField('brightness', validators=[DataRequired(), Length(3)])

    # feature_id = IntegerField('f_id', validators=[DataRequired(), NumberRange(min=1, max=40)])

    submit = SubmitField("Save")
