from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from ffanalytics import db, bcrypt, mail
#from ffanalytics.main.forms import
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime as dt
import secrets
import os
from PIL import Image

main = Blueprint('main',__name__)

## IMPORT DB MODEL
from ffanalytics.models import users,user_notes,user_note_changes


# Pages
@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user_pages.user_home'))
    return render_template('home.html',title='Home')
