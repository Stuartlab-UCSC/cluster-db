
import os

CLUSTERDB = os.environ.get("CLUSTERDB")

class Settings(object):
    # Flask:
    FLASK_SERVER_NAME = 'localhost:5555'
    FLASK_DEBUG = True  # Do not use debug mode in production

    # Flask-Restplus settings
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    
    # Application:
    DATABASE = os.path.join(CLUSTERDB, 'cluster.db')
    SECRET_KEY = os.environ.get("SECRET_KEY")
    USER_DATABASE = os.path.join(CLUSTERDB, 'cluster_user.db')
    UPLOADS = os.path.join(CLUSTERDB, 'uploads')
    VIEWER_URL = 'http://localhost:3000/'
