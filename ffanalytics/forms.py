from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    first_name = StringField('First Name', validators = [DataRequired(),Length(min=2,max=20)])
    last_name = StringField('Last Name', validators = [DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')