from ffanalytics import db, login_manager
from flask import current_app
from datetime import datetime as dt
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users(db.Model, UserMixin):
    __tablename__ = "users"

    #table Column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    user_notes = db.relationship('user_notes',backref='user',lazy=True)
    user_player_views = db.relationship('user_player_views', backref='user', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return users.query.get(user_id)

    def __repr__(self):
        return "users(email: '{}', first_name: '{}', last_name: '{}', join_date: '{}', image_file: '{}')".format(self.email,self.first_name,self.last_name,self.join_date,self.image_file)

class user_notes(db.Model):
    __tablename__ = "user_notes"

    #table Column
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

class stadium_details(db.Model):
    __tablename__ = "stadium_details"

    stadium_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(10))
    country = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stadium_type = db.Column(db.String(50))
    stadium_capacity = db.Column(db.Integer)
    stadium_surface = db.Column(db.String(25))
    active = db.Column(db.Integer)
    teams = db.relationship('team_details', backref='stadium_details', lazy=True)

    def __repr__(self):
        return f"stadium_details(stadium_id: {self.stadium_id}, name: {self.name}, city: {self.city}, state: {self.state})"

class team_details(db.Model):
    __tablename__ = "team_details"

    team_id = db.Column(db.Integer, primary_key=True)
    bye_week = db.Column(db.Integer)
    city = db.Column(db.String(100))
    conference = db.Column(db.String(3))
    division = db.Column(db.String(15))
    draft_kings_name = db.Column(db.String(50))
    draft_kings_player_id = db.Column(db.Integer)
    fan_duel_name = db.Column(db.String(50))
    fan_duel_player_id = db.Column(db.Integer)
    fantasy_draft_name = db.Column(db.String(50))
    fantasy_draft_player_id = db.Column(db.Integer)
    full_name = db.Column(db.String(50))
    global_team_id = db.Column(db.Integer)
    key = db.Column(db.String(10))
    name = db.Column(db.String(50))
    offensive_scheme = db.Column(db.String(10))
    primary_color = db.Column(db.String(10))
    quaternary_color = db.Column(db.String(10))
    secondary_color = db.Column(db.String(10))
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium_details.stadium_id'), nullable=False)
    tertiary_color = db.Column(db.String(10))
    wikipedia_logo_url = db.Column(db.String(1500))
    wikipedia_word_mark_url = db.Column(db.String(1500))
    yahoo_name = db.Column(db.String(50))
    yahoo_player_id = db.Column(db.Integer)
    teams = db.relationship('player_details', backref='team_details', lazy=True)

    def __repr__(self):
        return f"team_details(team_id: {self.team_id}, name: {self.city} {self.draft_kings_names}, conference: {self.conference}, division: {self.division})"


class player_details(db.Model):
    __tablename__ = "player_details"

    #table Column
    player_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    position = db.Column(db.String(25))
    position_category = db.Column(db.String(25))
    active = db.Column(db.Integer)
    current_team = db.Column(db.String(10))
    experience = db.Column(db.Integer)
    age = db.Column(db.Integer)
    team = db.Column(db.String(10))
    team_id = db.Column(db.Integer, db.ForeignKey('team_details.team_id'), nullable=False)
    height_feet = db.Column(db.Float)
    height_inches = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    average_draft_position = db.Column(db.Float)
    bye_week = db.Column(db.Integer)
    college = db.Column(db.String(255))
    draft_kings_name = db.Column(db.String(255))
    draft_kings_player_id = db.Column(db.Integer)
    fan_duel_name = db.Column(db.String(255))
    fan_duel_player_id = db.Column(db.Integer)
    fantasy_alarm_player_id = db.Column(db.Integer)
    fantasy_draft_name = db.Column(db.String(255))
    fantasy_draft_player_id = db.Column(db.Integer)
    fantasy_position = db.Column(db.String(255))
    photo_url = db.Column(db.String(1500))
    roto_wire_player_id = db.Column(db.Integer)
    rotoworld_player_id = db.Column(db.Integer)
    sport_radar_player_id = db.Column(db.Integer)
    sports_direct_player_id = db.Column(db.Integer)
    stats_player_id = db.Column(db.Integer)
    usa_today_player_id = db.Column(db.Integer)
    yahoo_name = db.Column(db.String(255))
    yahoo_player_id = db.Column(db.Integer)
    user_player_views = db.relationship('user_player_views', backref='player_details', lazy=True)

    def __repr__(self):
        return "player_details(name: {}, position: '{}', team: '{}')".format(self.name,self.position,self.team)

class user_player_views(db.Model):
    __tablename__ = "user_player_views"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player_details.player_id'), nullable=False)
    view_date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)

    def __repr__(self):
        return f"user_player_views(user_id: {self.user_id}, player_id: {self.player_id}, view_date: {self.view_date})"
