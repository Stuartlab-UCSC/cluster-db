import logging.config
import os
from cluster import settings
from flask import Flask, Blueprint, url_for
from flask_restplus import Api

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from cluster.auth.init import AuthConfigClass
from flask_admin import Admin
import datetime
from flask_babelex import Babel
from flask_cors import CORS
from flask_user import UserManager

from cluster.api.restplus import api
from cluster.database import db

from cluster.api.user import ns as user_namespace
from cluster.api.sql import ns as sql_namespace
from cluster.api.cluster_solution import ns as cluster_solution_namespace
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.marker import ns as marker_namespace
from cluster.api.dotplot import ns as dotplot_namespace

from cluster.database.default_entries import entries as default_entries
from cluster.database.add_entries import add_entries
from cluster.database.user_models import *

# monkey patch so that /swagger.json is served over https
# grabbed from https://github.com/noirbizarre/flask-restplus/issues/54
if os.environ.get('HTTPS'):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')

    Api.specs_url = specs_url


def configure_app(flask_app, test_config):
    if test_config is None:
        # load the instance config, if it exists, when not testing
        flask_app.config.from_mapping(
            #SERVER_NAME = settings.SERVER_NAME,
            RESTPLUS_VALIDATE= settings.RESTPLUS_VALIDATE,
            RESTPLUS_MASK_SWAGGER= settings.RESTPLUS_MASK_SWAGGER,
            DATABASE= settings.DATABASE, # for pre_sqlAlchemy.py
            SQLALCHEMY_DATABASE_URI= "sqlite:///" + settings.DATABASE,
            SQLALCHEMY_BINDS = {"users": "sqlite:///" + settings.USER_DATABASE},
            UPLOADS= settings.UPLOADS,
        )
        flask_app.config['VIEWER_URL'] = os.environ.get('VIEWER_URL')
        flask_app.config.from_object(AuthConfigClass)
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
    global apiBlueprint
    if (apiBlueprint):
        return
    apiBlueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(apiBlueprint)

    api.add_namespace(cluster_solution_namespace)
    api.add_namespace(dataset_namespace)
    api.add_namespace(dotplot_namespace)
    api.add_namespace(marker_namespace)
    api.add_namespace(sql_namespace)
    api.add_namespace(user_namespace)

    app.register_blueprint(apiBlueprint)


def setup_logger(logfile='../logging.conf'):
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), logfile))
    logging.config.fileConfig(logging_conf_path)
    logging.getLogger(__name__)


def create_app(extra_config={}):

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    app.config.update(extra_config)


    CORS(app)
    Babel(app)

    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_BINDS'] = \
        {"users": app.config["SQLALCHEMY_USER_DATABASE_URI"]}

    initialize_blueprint(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        user_manager = UserManager(app, db, User)

        if not app.testing:
            setup_logger()
            user = {
                "email": "test@test.com",
                "password": user_manager.hash_password("testT1234"),
                "email_confirmed_at": datetime.datetime.utcnow(),

            }
            default_entries.append((User, user))
            add_entries(db.session, default_entries)

    return app


if __name__ == "__main__":
    create_app()
