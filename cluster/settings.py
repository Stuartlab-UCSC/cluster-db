import os


def directory_back_from_this_file():
    return os.path.join(
        os.path.split(
            os.path.split(os.path.abspath(__file__))[0]
        )
    [0], "instance")

# Used for default location of database
CLUSTERDB = os.path.join(directory_back_from_this_file(), "cluster.db")
USERDB = os.path.join(directory_back_from_this_file(), "cluster_user.db")
VIEWER_URL = os.environ.get("VIEWER_URL", "localhost:3000/")
USER_DIRECTORY = os.path.join(directory_back_from_this_file(), "users")
# Flask settings
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)

SQLALCHEMY_DATABASE_URI="sqlite:///" + CLUSTERDB
SQLALCHEMY_USER_DATABASE_URI="sqlite:///" + USERDB
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

# FLASK-USER CONFIG:
# https://flask-user.readthedocs.io/en/latest/configuring_settings.html

# Flask settings
SECRET_KEY = os.environ.get(
    "CLUSTERDB_SECRET_KEY",
    default='This is an INSECURE secret!! DO NOT use this in production!!'
)

USER_USER_SESSION_EXPIRATION = 604800

# Flask-Sendmail settings
DEFAULT_MAIL_SENDER = os.environ.get("CLUSTERDB_EMAIL")
DEFAULT_MAX_EMAILS = 5

# Features
USER_ENABLE_USERNAME = False  # email auth only, no username is used

# Generic
USER_APP_NAME = "UCSC Cell Atlas"  # in and email templates and page footers
USER_AUTO_LOGIN = True
USER_AUTO_LOGIN_AFTER_REGISTER = False
USER_AUTO_LOGIN_AT_LOGIN = False
USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = 'hexmap@ucsc.edu'

# Endpoints
USER_EDIT_USER_PROFILE_URL = '/user/change-password'
USER_AFTER_CHANGE_PASSWORD_ENDPOINT = 'user.login'
USER_AFTER_CONFIRM_ENDPOINT = 'user.login'
USER_AFTER_FORGOT_PASSWORD_ENDPOINT = 'check_email'
USER_AFTER_LOGIN_ENDPOINT = 'after_login'
USER_AFTER_LOGOUT_ENDPOINT = 'after_logout'
USER_AFTER_REGISTER_ENDPOINT = 'check_email'
USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = 'check_email'
USER_AFTER_RESET_PASSWORD_ENDPOINT = 'check_email'
USER_UNAUTHENTICATED_ENDPOINT = 'user.login'
USER_UNAUTHORIZED_ENDPOINT = 'unauthorized'
