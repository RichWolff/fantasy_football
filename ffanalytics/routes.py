from flask import render_template, url_for, flash, redirect, request
from ffanalytics import app, db, bcrypt
from ffanalytics.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route('/account')
@login_required
def account():
    return render_template('account.html',title='Account')
