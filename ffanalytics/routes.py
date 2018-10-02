from flask import render_template, url_for, flash, redirect, request, abort
from ffanalytics import app, db, bcrypt
from ffanalytics.forms import RegistrationForm, LoginForm, UpdateAccountForm, UserNoteForm
from flask_login import login_user, current_user, logout_user, login_required
import datetime as dt
import secrets
import os
from PIL import Image


## IMPORT DB MODEL
from ffanalytics.models import users,user_notes,user_note_changes


# Pages
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user_home'))
    return render_template('home.html',title='Home')


@login_required
@app.route('/user/home', methods=['GET', 'POST'])
def user_home():
    user_note_form = UserNoteForm()
    if user_note_form.validate_on_submit():

        new_content = user_notes(
            user_id=current_user.id,
            content=user_note_form.content.data)
        db.session.add(new_content)
        new_content = user_notes.query.filter_by(user_id=current_user.id).order_by(user_notes.note_date.desc()).first()
        res = track_note_changes(note_id = new_content.id,
                         modify_type = 'Create',
                         modify_date = new_content.note_date,
                         new_content = new_content.content)

        if res == 0:

            db.session.commit()
            flash('Note has been updated.','success')
            return redirect(url_for('user_home'))

        else:
            db.session.rollback()
            db.session.remove()
            flash('Note not saved, something wen\'t wrong','failure')


    updates = get_user_activity()
    return render_template('user_page.html',
                            title='User Home',
                            user_note_form = user_note_form,
                            user_notes = updates,
                            legend = 'Add a Note')

def get_user_activity():
    return user_notes.query.filter_by(user_id=current_user.id,note_active=1).order_by(user_notes.note_date.desc())

def track_note_changes(note_id,modify_type,modify_date,new_content,old_content=''):
    #update post tracking
    try:
        new_content_update = user_note_changes(
                note_id = note_id,
                modify_type = modify_type,
                modify_date = modify_date,
                old_content = old_content,
                new_content = new_content,
            )

        db.session.add(new_content_update)
    except Exception as e:
        return 1
    else:
        return 0

@login_required
@app.route('/user/home/edit_note_<int:user_note_id>', methods=['GET', 'POST'])
def user_note_update(user_note_id):
    user_note = user_notes.query.get_or_404(user_note_id)

    if not user_note.user == current_user:
        abort(403)

    user_note_form = UserNoteForm()

    pull_updates_into_form = 1

    if user_note_form.validate_on_submit():

        #set variables for updates to be made
        old_content = user_note.content
        new_content = user_note_form.content.data

        if old_content == new_content:
            flash('No changes made to note.','warning')

        elif not old_content == new_content:
            update_dt = dt.datetime.now()

            #update post
            user_note.content = new_content
            user_note.note_last_changed = update_dt

            pull_updates_into_form = track_note_changes(note_id = user_note.id,
                                     modify_type = 'Update',
                                     modify_date = update_dt,
                                     new_content = new_content,
                                     old_content = old_content)

            if pull_updates_into_form == 0:
                db.session.commit()
                flash('Note has been updated.','success')
                return redirect(url_for('user_home'))
            else:
                db.session.rollback()
                db.session.remove()
                flash('Note not saved, something wen\'t wrong','failure')


    if pull_updates_into_form == 1:
        user_note_form.content.data = user_note.content

    updates = get_user_activity()

    return render_template('user_page.html',
                            title='Update Note',
                            note_to_update=user_note,
                            user_notes=updates,
                            user_note_form=user_note_form,
                            legend = 'Update Note')

@app.route('/user/home/delete_note_<int:user_note_id>', methods=['POST'])
@login_required
def delete_note(user_note_id):
    user_note = user_notes.query.get_or_404(user_note_id)

    if not user_note.user == current_user:
        abort(403)

    pull_updates_into_form = track_note_changes(note_id = user_note.id,
                         modify_type = 'Deactivate',
                         modify_date = dt.datetime.now(),
                         new_content = user_note.content,
                         old_content = user_note.content)

    if pull_updates_into_form == 0:
        user_note.note_active = 0
        db.session.commit()
        flash('Note has been deleted.','success')
        return redirect(url_for('user_home'))
    else:
        db.session.rollback()
        db.session.remove()
        flash('Note not saved, something wen\'t wrong','failure')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_home'))

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
            return redirect(url_for('user_home'))
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






