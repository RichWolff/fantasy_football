from flask import render_template, url_for, flash, redirect, request
from ffanalytics import app, db, bcrypt
from ffanalytics.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
#from datetime import dt
# A very simple Flask Hello World app for you to get started with...
## IMPORT DB MODEL
from ffanalytics.models import users,user_notes,user_note_changes


# Pages
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        #Check login
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    #Rename file name using random filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex)+ str(f_ext)
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.image_file = picture_file
        if not form.first_name.data == current_user.first_name:
            current_user.first_name = form.first_name.data
        if not form.last_name.data == current_user.last_name:
            current_user.last_name = form.last_name.data
        if not form.email.data == current_user.email:
            current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
