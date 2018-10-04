from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ffanalytics.models import users
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    first_name = StringField('First Name', validators = [DataRequired(),Length(min=2,max=20)])
    last_name = StringField('Last Name', validators = [DataRequired(),Length(min=2,max=20)])
    profile_picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png','gif'])])
    submit = SubmitField('Update Account')

    def validate_email(self,email):
        if not email.data == current_user.email:
            user = users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please login with your existing account.')

class UserNoteForm(FlaskForm):
    content = TextAreaField('Add Some Thoughts', validators = [DataRequired(),Length(min=5,max=255)])
    submit = SubmitField('Save Note')
