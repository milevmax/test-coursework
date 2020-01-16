from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email

class UserForm(FlaskForm):

    user_name = StringField('name', validators=[DataRequired(), Length(2)])

    user_age = IntegerField('age', validators=[DataRequired(), NumberRange(min=18, max=100)])

    user_email = StringField('email', validators=[DataRequired(), Email("Wrong email format")])

    skin_condition = IntegerField('skin(rate by whole number from 1 to 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])

    eye_color = SelectField('eye color',choices=[('blue','blue'),
                                                 ('gray','gray'),
                                                 ('brown','brown'),
                                                 ('green','green')], validators=[DataRequired("Please enter your eye color.")])

    hair_color = SelectField('hair color',choices=[('brunette','brunette'),
                                            ('blonde','blonde'),
                                            ('brown','brown'),
                                            ('red','red')], validators=[DataRequired("Please enter your hair color.")])

    lips_color = SelectField('lips color',choices=[('saturated','saturated'),
                                                   ('unsaturated','unsaturated')], validators=[DataRequired("Please enter your lips color.")])

    skin_tone = SelectField('skin tone',choices=[('gray','gray'),
                                                 ('pale','pale'),
                                                 ('pink','pink'),
                                                 ('dark','dark')], validators=[DataRequired("Please enter your skin tone.")])

    submit = SubmitField("Save")

