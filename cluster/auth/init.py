# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask_babelex import Babel

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

    # Flask-User settings
    USER_AFTER_LOGIN_ENDPOINT = 'after_login'
    USER_AFTER_LOGOUT_ENDPOINT = 'after_logout'
    USER_APP_NAME = "UCSC Cell Atlas" # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

    # FLASK-USER CONFIG:
    # https://flask-user.readthedocs.io/en/latest/configuring_settings.html

def auth_init(app):
    app.config.from_object(__name__+'.ConfigClass')
    
    # Initialize Flask-BabelEx
    Babel(app)
