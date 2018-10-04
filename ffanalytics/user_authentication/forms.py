from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ffanalytics.models import users

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



class RequestResetForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Change Password')