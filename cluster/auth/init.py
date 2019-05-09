# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask_babelex import Babel
from flask_user import UserManager
from cluster import settings
#from cluster.auth.accounts import default_auth_accounts
from cluster.auth.routes import auth_routes
from cluster.auth.db_models import User

# Class-based application configuration
class ConfigClass(object):

    # FLASK-USER CONFIG:
    # https://flask-user.readthedocs.io/en/latest/configuring_settings.html

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
    USER_ENABLE_USERNAME = False # email auth only, no username is used
    
    # Generic
    USER_APP_NAME = "UCSC Cell Atlas" # in and email templates and page footers
    USER_AUTO_LOGIN = False
    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_AUTO_LOGIN_AT_LOGIN = False
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'
    
    # URLs
    USER_EDIT_USER_PROFILE_URL = '/user/change-password'
    
    # Endpoints

    USER_AFTER_CHANGE_PASSWORD_ENDPOINT           = 'home'
    USER_AFTER_CONFIRM_ENDPOINT                   = 'user.login'
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT           = 'home'
    USER_AFTER_LOGIN_ENDPOINT                     = 'after_login'
    USER_AFTER_LOGOUT_ENDPOINT                    = 'after_logout'
    USER_AFTER_REGISTER_ENDPOINT                  = 'home'
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = 'home'
    USER_AFTER_RESET_PASSWORD_ENDPOINT            = 'home'
    USER_UNAUTHENTICATED_ENDPOINT                 = 'user.login'
    USER_UNAUTHORIZED_ENDPOINT                    = 'unauthorized'

def auth_init(app, db):
    app.config.from_object(__name__+'.ConfigClass')
    
    # Initialize Flask-BabelEx
    Babel(app)

    # Create the user database.
    db.create_all(bind='users')

    # Create the user manager.
    UserManager(app, db, User)

    # Create the default admin account on initial DB creation.
    #default_auth_accounts(app, db)  # for initial admin account
    
    # Define the auth routes,
    auth_routes(app, db)
