# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask_babelex import Babel
from cluster import settings
from cluster.auth.accounts import default_auth_accounts
from cluster.auth.routes import auth_routes

# Class-based application configuration
class ConfigClass(object):

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'hexmap@ucsc.edu'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'

    # Features
    USER_ENABLE_USERNAME = False    # Disable username authentication
    
    # Generic
    USER_APP_NAME = "UCSC Cell Atlas" # Shown in and email templates and page footers
    USER_AUTO_LOGIN = False
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'
    USER_SHOW_USERNAME_DOES_NOT_EXIST = True
    
    # Endpoints
    USER_AFTER_LOGIN_ENDPOINT = 'after_login'
    USER_AFTER_LOGOUT_ENDPOINT = 'after_logout'
    #USER_AFTER_REGISTER_ENDPOINT = 'after_login'

    # FLASK-USER CONFIG:
    # https://flask-user.readthedocs.io/en/latest/configuring_settings.html

def auth_init(app, db):
    app.config.from_object(__name__+'.ConfigClass')
    
    # Initialize Flask-BabelEx
    Babel(app)

    # Create the user database.
    db.create_all(bind='users')

    default_auth_accounts(app, db)
    auth_routes(app, db)
