from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ffanalytics.models import users
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    first_name = StringField('First Name', validators = [DataRequired(),Length(min=2,max=20)])
    last_name = StringField('Last Name', validators = [DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        user = users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please login with your existing account.')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

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