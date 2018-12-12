
# app.py

import logging.config
import os
from cluster import settings
from flask import Flask, Blueprint, redirect
from cluster.api.clustering import ns as clustering_namespace
from cluster.api.dataset import ns as dataset_namespace
#from cluster.api.signature_gene import ns as signature_gene_namespace
#from cluster.api.signature_gene_set import ns as signature_gene_set_namespace
from cluster.api.restplus import api, init as api_init
import cluster.database.db as db

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
            ERROR_404_HELP = settings.RESTPLUS_ERROR_404_HELP,
            DATABASE = settings.DATABASE,
            UPLOADS = settings.UPLOADS,
        )
        # Doesn't work:
        #flask_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flask_app.config.from_mapping(test_config)
        flask_app.config['DEBUG'] = False
        if flask_app.config['DATABASE'] == None:
            flask_app.config['DATABASE'] = '/tmp'

    # Ensure the instance folder exists, if we are using one.
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass


def initialize_blueprint(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(clustering_namespace)
    api.add_namespace(dataset_namespace)
    #api.add_namespace(signature_gene_namespace)
    #api.add_namespace(signature_gene_set_namespace)
    flask_app.register_blueprint(blueprint)


def initialize_app(flask_app, test_config):
    configure_app(flask_app, test_config)
    initialize_blueprint(flask_app)
    with flask_app.app_context():
        db.init_db()
        api_init(flask_app)


def create_app(test_config=None):
    app = Flask(__name__)
    #app = Flask(__name__, instance_relative_config=True)
    initialize_app(app, test_config)
    #log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

    # Handle the base route.
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
