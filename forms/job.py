from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = StringField('Leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = StringField('Size', validators=[DataRequired()])
    collaborators = StringField('Coworkers', validators=[DataRequired()])
    submit = SubmitField('Add')


class EditJobForm(FlaskForm):
    team_leader = StringField('Leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = StringField('Size', validators=[DataRequired()])
    collaborators = StringField('Coworkers', validators=[DataRequired()])
    submit = SubmitField('Edit')
