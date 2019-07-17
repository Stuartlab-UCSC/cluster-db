
import os

# Flask settings
FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
#SERVER_NAME = os.environ.get('FLASK_SERVER_NAME')

# Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False

# Application settings
DATABASE = os.path.join(os.environ.get("CLUSTERDB"), 'cluster.db')
USER_DATABASE = os.path.join(os.environ.get("CLUSTERDB"), 'cluster_user.db')
UPLOADS = os.path.join(os.environ.get("CLUSTERDB"), 'uploads')
