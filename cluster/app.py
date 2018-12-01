
# app.py

import logging.config

import os
from flask import Flask, Blueprint
from cluster import settings
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.todo import ns as todo_namespace
from cluster.api.restplus import api
import cluster.database.tableBase as db

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


def initialize_blueprint(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(dataset_namespace)
    api.add_namespace(todo_namespace)
    flask_app.register_blueprint(blueprint)


def initialize_app(flask_app):
    configure_app(flask_app)
    initialize_blueprint(flask_app)
    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
