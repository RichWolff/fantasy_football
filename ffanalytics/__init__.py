
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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

## Import routes after to avoid circular ref
from ffanalytics import routes
