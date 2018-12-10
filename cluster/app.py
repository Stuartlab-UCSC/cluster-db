
# app.py

import logging.config

import os
from flask import Flask, Blueprint, redirect
from cluster import settings
from cluster.api.clustering import ns as clustering_namespace
from cluster.api.dataset import ns as dataset_namespace
#from cluster.api.signature_gene import ns as signature_gene_namespace
#from cluster.api.signature_gene_set import ns as signature_gene_set_namespace
from cluster.api.restplus import api, init as apiInit
import cluster.database.db as db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['DATABASE'] = settings.DATABASE
    flask_app.config['UPLOADS'] = settings.UPLOADS


def initialize_blueprint(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(clustering_namespace)
    api.add_namespace(dataset_namespace)
    #api.add_namespace(signature_gene_namespace)
    #api.add_namespace(signature_gene_set_namespace)
    flask_app.register_blueprint(blueprint)


def initialize_app(flask_app):
    configure_app(flask_app)
    initialize_blueprint(flask_app)
    with app.app_context():
        db.init_db()
        apiInit(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


# Handle the base route.
@app.route('/')
def baseRoute():
    return redirect("/api", code=302)


# Handle the test route.
@app.route('/test')
def testRoute():
    return 'Just testing the clusterDb server'


if __name__ == "__main__":
    main()
