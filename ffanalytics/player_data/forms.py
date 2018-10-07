from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ffanalytics.models import users
from flask_login import current_user


class PlayerSearchForm(FlaskForm):
    player_name = StringField('Player Name')
    position = StringField('Player Position')
    team = StringField('Player Team')
    submit = SubmitField('Search')
