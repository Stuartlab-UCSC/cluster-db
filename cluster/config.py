
import os

# Flask settings
FLASK_DEBUG = True  # Do not use debug mode in production
SERVER_NAME = 'localhost:5555'

# Flask-Restplus settings
ERROR_404_HELP = False
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'list'

# Application settings
CLUSTERDB = os.environ['CLUSTERDB']
DATABASE = CLUSTERDB + '../cluster.db'
UPLOADS = CLUSTERDB + '../uploads'
