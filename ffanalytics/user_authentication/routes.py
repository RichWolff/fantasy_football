from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from ffanalytics import db, bcrypt, mail
from ffanalytics.user_authentication.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime as dt
import secrets
import os
from PIL import Image

user_authentication = Blueprint('user_authentication', __name__)

## IMPORT DB MODEL
from ffanalytics.models import users,user_notes,user_note_changes


# Pages

@user_authentication.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_pages.user_home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        # Generate new users object and save to database
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = users(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # Return
        flash('Account created for {}! Please login using the credentials supplied.'.format(form.email.data), 'success')
        return redirect(url_for('user_authentication.login'))
    return render_template('register.html',title='Register',form=form)


@user_authentication.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('user_pages.user_home'))
    form = LoginForm()
    if form.validate_on_submit():

        #Check login
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html',title='Login',form=form)


@user_authentication.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#Forgot password/Reset Password

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Fantasy Football Analytics Password Reset Request',
                    sender='ffanalytics4@gmail.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('user_authentication.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.'''.format(token)
    mail.send(msg)
    return None

@user_authentication.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('user_pages.user_home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('user_authentication.login'))

    return render_template('reset_request.html', title='Reset Password',form=form)

@user_authentication.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('user_pages.user_home'))

    user = users.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired link.','warning')
        return redirect(url_for('user_authentication.reset_request'))


    form = ResetPasswordForm()
    if form.validate_on_submit():

        # Generate new users object and save to database
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()

        # Return
        flash('Your password has been updated! Please login using your new password.', 'success')
        return redirect(url_for('user_authentication.login'))

    return render_template('reset_password.html', title='Reset Password',form=form)



