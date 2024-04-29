from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class DepForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chief = StringField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Add')