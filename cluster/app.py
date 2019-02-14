
# app.py

import logging.config
import os
from cluster import settings
from flask import Flask, Blueprint, redirect
from flask_cors import CORS
from cluster.api.query import ns as query_namespace
from cluster.api.restplus import api
import cluster.database.db as db

CLUSTERDB_UPDATABLE = 0
try:
    CLUSTERDB_UPDATABLE = int(os.environ['CLUSTERDB_UPDATABLE'])
except:
    pass
if CLUSTERDB_UPDATABLE > 0:
    from cluster.api.attribute import ns as attribute_namespace
    from cluster.api.cluster import ns as cluster_namespace
    from cluster.api.cell_assignment import ns as cell_assignment_namespace
    from cluster.api.cluster_solution import ns as cluster_solution_namespace
    from cluster.api.dataset import ns as dataset_namespace
    from cluster.api.signature_gene import ns as signature_gene_namespace
    from cluster.api.signature_gene_set import ns as signature_gene_set_namespace

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app, test_config):

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flask_app.config.from_mapping(
            SECRET_KEY='dev',
            #SERVER_NAME = settings.FLASK_SERVER_NAME,
            RESTPLUS_VALIDATE = settings.RESTPLUS_VALIDATE,
            RESTPLUS_MASK_SWAGGER = settings.RESTPLUS_MASK_SWAGGER,
            DATABASE = settings.DATABASE,
            UPLOADS = settings.UPLOADS,
        )
        # Doesn't work:
        #flask_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flask_app.config.from_mapping(test_config)
        flask_app.config['DEBUG'] = False

    # Ensure the instance folder exists, if we are using one.
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass


def initialize_blueprint(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(query_namespace)
    if CLUSTERDB_UPDATABLE > 0:
        if not flask_app.config['TESTING']:
            logging.warning('!!!!!!  DATABASE UPDATABLE !!!!!!')
        api.add_namespace(attribute_namespace)
        api.add_namespace(cell_assignment_namespace)
        api.add_namespace(cluster_namespace)
        api.add_namespace(cluster_solution_namespace)
        api.add_namespace(dataset_namespace)
        api.add_namespace(signature_gene_namespace)
        api.add_namespace(signature_gene_set_namespace)
    
    flask_app.register_blueprint(blueprint)

def initialize_app(flask_app, test_config):
    configure_app(flask_app, test_config)
    initialize_blueprint(flask_app)
    with flask_app.app_context():
        db.init_db()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.url_map.strict_slashes = False
    #app = Flask(__name__, instance_relative_config=True)
    initialize_app(app, test_config)
    #log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

    # Handle the base route, redirecting to /api.
    @app.route('/')
    def baseRoute():
        return redirect("/api", code=302)

    # Handle the test route.
    @app.route('/test')
    def testRoute():
        return 'Just testing the clusterDb server'

    return app


if __name__ == "__main__":
    create_app()
