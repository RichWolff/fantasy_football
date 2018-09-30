
# A very simple Flask Hello World app for you to get started with...
from datetime import datetime as dt
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = 'e1b111968e5524643df879a0e5d11fc4'


## Database Constants
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="richwolff",
    password="#4BobbyOrr",
    hostname="richwolff.mysql.pythonanywhere-services.com",
    databasename="richwolff$fantasy_football",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)


## IMPORT DB MODEL
from models import users,user_notes,user_note_changes


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