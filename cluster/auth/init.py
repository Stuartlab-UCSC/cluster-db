
class AuthConfigClass(object):

    # FLASK-USER CONFIG:
    # https://flask-user.readthedocs.io/en/latest/configuring_settings.html

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
