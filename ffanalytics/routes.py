from flask import render_template, url_for, flash, redirect
from ffanalytics import app
from ffanalytics.forms import RegistrationForm, LoginForm
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.email.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logged_in=False
        if logged_in:
            flash('Successfully logged in as {}!'.format(form.email.data), 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html',title='Login',form=form)
