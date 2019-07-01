import os


# Used for default location of database
CLUSTERDB = os.path.split(
        os.path.split(os.path.abspath(__file__))[0]
    )[0]

# Flask settings
FLASK_DEBUG = True
SECRET_KEY = "super secret key"
SQLALCHEMY_DATABASE_URI="sqlite://" / CLUSTERDB
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

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