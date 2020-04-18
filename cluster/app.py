import logging.config
import os
from flask import Flask, Blueprint, url_for
from flask_restplus import Api

from flask_babelex import Babel
from flask_cors import CORS
from flask_user import UserManager
from cluster import admin
from cluster.cli.cli import command_line_interface

from cluster.api.restplus import api
from cluster.database import db

from cluster.api.user import ns as user_namespace
from cluster.api.sql import ns as sql_namespace
from cluster.api.cluster_solution import ns as cluster_solution_namespace
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.marker import ns as marker_namespace
from cluster.api.dotplot import ns as dotplot_namespace
from cluster.api.scorect import ns as scorect_namespace
from cluster.api.auth import auth_routes

from cluster.database.user_models import User


# monkey patch so that /swagger.json is served over https
# grabbed from https://github.com/noirbizarre/flask-restplus/issues/54
if os.environ.get('HTTPS'):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    Api.specs_url = specs_url


def initialize_blueprint(flask_app):
    apiBlueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(apiBlueprint)

    api.add_namespace(scorect_namespace)
    api.add_namespace(cluster_solution_namespace)
    api.add_namespace(dataset_namespace)
    api.add_namespace(dotplot_namespace)
    api.add_namespace(marker_namespace)
    api.add_namespace(sql_namespace)
    api.add_namespace(user_namespace)

    flask_app.register_blueprint(apiBlueprint)


def setup_logger(logfile='../logging.conf'):
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), logfile))
    logging.config.fileConfig(logging_conf_path)
    logging.getLogger(__name__)


@command_line_interface
def create_app(config={}):

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    app.config.update(config)

    CORS(app, supports_credentials=True)
    Babel(app)

    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_BINDS'] = \
        {"users": app.config["SQLALCHEMY_USER_DATABASE_URI"]}
    auth_routes(app)
    initialize_blueprint(app)

    db.init_app(app)
    admin.init_app(app, db)

    with app.app_context():
        db.create_all()
        user_manager = UserManager(app, db, User)
        from flask_user.email_adapters import SendmailEmailAdapter
        user_manager.email_adapter = SendmailEmailAdapter(app)
  
    if not app.testing:
        setup_logger()

    return app

if __name__ == "__main__":
    create_app()
