from ffanalytics import db, login_manager, app
from datetime import datetime as dt
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users(db.Model, UserMixin):
    __tablename__ = "users"

    #table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    user_notes = db.relationship('user_notes',backref='user',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return users.query.get(user_id)

    def __repr__(self):
        return "users(email: '{}', first_name: '{}', last_name: '{}', join_date: '{}', image_file: '{}')".format(self.email,self.first_name,self.last_name,self.join_date,self.image_file)

class user_notes(db.Model):
    __tablename__ = "user_notes"

    #table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    note_last_changed = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    content = db.Column(db.Text, nullable=False)
    note_active = db.Column(db.Integer, nullable=False, default=1)
    note_changes = db.relationship('user_note_changes', backref='note', lazy=True)


    def __repr__(self):
        return "user_note(user_id: '{}', note_date: '{}', note_last_changed: '{}', note_active: {})".format(self.user_id,self.note_date,self.note_last_changed,self.note_active)


class user_note_changes(db.Model):
    __tablename__ = 'user_note_changes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('user_notes.id'),nullable=False)
    modify_type = db.Column(db.String(25),unique=False,nullable=True)
    modify_date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    old_content = db.Column(db.Text, nullable=False)
    new_content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "user_note_changes(note_id: {}, modify_type: '{}', modify_date: '{}')".format(self.note_id,self.modify_type,self.modify_date)
