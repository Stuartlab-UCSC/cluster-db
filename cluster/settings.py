import os


def directory_back_from_this_file():
    return os.path.split(
        os.path.split(os.path.abspath(__file__))[0]
    )[0]

# Used for default location of database
CLUSTERDB = os.path.join(directory_back_from_this_file(), "cluster.db")
USERDB = os.path.join(directory_back_from_this_file(), "cluster_user.db")
VIEWER_URL = os.environ.get("VIEWER_URL", "localhost:3000/")
USER_DIRECTORY = os.path.join(directory_back_from_this_file(), "users")
# Flask settings

FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
#SERVER_NAME = os.environ.get('FLASK_SERVER_NAME')

# Restplus settings
FLASK_DEBUG = True
SECRET_KEY = "super secret key"
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

# Flask-Mail SMTP server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465

MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.environ.get("CLUSTERDB_EMAIL")
MAIL_PASSWORD = os.environ.get("CLUSTERDB_EMAIL_PW")

if MAIL_PASSWORD is None or MAIL_USERNAME is None:
    USER_ENABLE_EMAIL = False

MAIL_DEFAULT_SENDER = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'
DEFAULT_MAIL_SENDER = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'

# Features
USER_ENABLE_USERNAME = False  # email auth only, no username is used

# Generic
USER_APP_NAME = "UCSC Cell Atlas"  # in and email templates and page footers
USER_AUTO_LOGIN = False
USER_AUTO_LOGIN_AFTER_REGISTER = False
USER_AUTO_LOGIN_AT_LOGIN = False
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = '"UCSC Cell Atlas" <hexmap@ucsc.edu>'

USER_EDIT_USER_PROFILE_URL = '/user/change-password'

# Endpoints
USER_AFTER_CHANGE_PASSWORD_ENDPOINT = 'home'
USER_AFTER_CONFIRM_ENDPOINT = 'user.login'
USER_AFTER_FORGOT_PASSWORD_ENDPOINT = 'home'
USER_AFTER_LOGIN_ENDPOINT = 'after_login'
USER_AFTER_LOGOUT_ENDPOINT = 'after_logout'
USER_AFTER_REGISTER_ENDPOINT = 'home'
USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = 'home'
USER_AFTER_RESET_PASSWORD_ENDPOINT = 'home'
USER_UNAUTHENTICATED_ENDPOINT = 'user.login'
USER_UNAUTHORIZED_ENDPOINT = 'unauthorized'