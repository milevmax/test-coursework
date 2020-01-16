from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,SelectField
from wtforms.validators import DataRequired, NumberRange, Length


class RemedyForm(FlaskForm):

    # remedy_id = IntegerField('id', validators=[DataRequired(), NumberRange(min=1, max=20)])

    remedy_name = StringField('name', validators=[DataRequired(), Length(3)])

    remedy_color = StringField('color', validators=[DataRequired(), Length(2)])

    remedy_brightness = SelectField('intensity',choices=[('low','low'), ('medium','medium'), ('strong', 'strong')], validators=[DataRequired("Please enter intensity.")])

    # feature_id = IntegerField('f_id', validators=[DataRequired(), NumberRange(min=1, max=40)])

    submit = SubmitField("Save")
