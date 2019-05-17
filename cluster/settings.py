
import os

CLUSTERDB = os.environ.get("CLUSTERDB")

class Settings(object):
    
    # Application:
    DATABASE = os.path.join(CLUSTERDB, 'cluster.db')
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOADS = os.path.join(CLUSTERDB, 'uploads')
    USER_DATABASE = os.path.join(CLUSTERDB, 'cluster_user.db')
    VIEWER_URL = 'http://localhost:3000/'
    
    # SQL Alchemy:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Restplus settings
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False

    # Flask:
    FLASK_SERVER_NAME = 'localhost:5555'
    FLASK_DEBUG = True  # Do not use debug mode in production
