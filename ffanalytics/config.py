import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


    ## Database Constants
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
        username = os.environ.get('DB_USERNAME'),
        password = os.environ.get('DB_PASSWORD'),
        hostname="richwolff.mysql.pythonanywhere-services.com",
        databasename="richwolff$fantasy_football",
    )
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #email config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')