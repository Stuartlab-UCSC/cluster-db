
import os

# Flask settings
FLASK_SERVER_NAME = 'localhost:5555'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

# Application settings
DATABASE = os.path.join(os.environ.get("CLUSTERDB"), 'cluster.db')
UPLOADS = os.path.join(os.environ.get("CLUSTERDB"), 'uploads')
