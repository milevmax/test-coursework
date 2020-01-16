from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length


class FeatureForm(FlaskForm):

    feature_name = StringField('name', validators=[DataRequired(), Length(2)])

    feature_size = SelectField('size',choices=[('big','big'), ('medium','medium'), ('small','small')], validators=[DataRequired("Please enter your age.")])

    formtype = StringField('form description',  validators=[DataRequired("Please enter type of feature.")])

    submit = SubmitField("Save")



#
#     feature_name = StringField('name', validators=[DataRequired(), Length(3)])
#
#     feature_size = StringField('size', validators=[DataRequired(), Length(3)])
#
#     formtype = IntegerField('formtype', validators=[DataRequired(), NumberRange(min=1, max=10)])
#
#     submit = SubmitField("Save")