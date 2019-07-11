# app.py

import logging.config
import os
from cluster import settings
from flask import Flask, Blueprint, url_for
from flask_restplus import Api

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from cluster.auth.init import AuthConfigClass
from flask_admin import Admin
from flask_babelex import Babel
from flask_user import UserManager
from cluster.auth.db_models import User
from cluster.auth.accounts import auth_temporary_account
from cluster.auth.routes import auth_routes
from cluster.auth.admin import admin_init
from cluster.api.sql import ns as sql_namespace
from cluster.api.restplus import api
from cluster.api.cluster_attribute import ns as cluster_attribute_namespace
from cluster.api.cluster import ns as cluster_namespace
from cluster.api.cell_of_cluster import ns as cell_of_cluster_namespace
from cluster.api.cluster_solution import ns as cluster_solution_namespace
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.gene_of_set import ns as gene_of_set_namespace
from cluster.api.gene_set import ns as gene_set_namespace
from cluster.api.marker import ns as marker_namespace
from cluster.api.dotplot import ns as dotplot_namespace
from cluster.api.user import ns as user_namespace
from cluster.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
apiBlueprint = 0
userManager = 0

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
            #SERVER_NAME = settings.FLASK_SERVER_NAME,
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
    api.add_namespace(cell_of_cluster_namespace)
    api.add_namespace(cluster_attribute_namespace)
    api.add_namespace(cluster_namespace)
    api.add_namespace(cluster_solution_namespace)
    api.add_namespace(dataset_namespace)
    api.add_namespace(dotplot_namespace)
    api.add_namespace(gene_of_set_namespace)
    api.add_namespace(gene_set_namespace)
    api.add_namespace(marker_namespace)
    api.add_namespace(sql_namespace)
    api.add_namespace(user_namespace)


    apiBlueprint = flask_app.register_blueprint(apiBlueprint)


def initialize_app(flask_app, test_config):
    configure_app(flask_app, test_config)
    db.init_app(flask_app)
    Babel(flask_app) # for auth at least
    initialize_blueprint(flask_app)
    admin = Admin(flask_app, name='CellAtlas Admin', template_mode='bootstrap3')
    admin_init(db, admin)

    with flask_app.app_context():
        db.create_all()
        global userManager
        if (not userManager):
            userManager = UserManager(flask_app, db, User)
            auth_temporary_account(flask_app, db, userManager)
            auth_routes(flask_app, db)


def create_app(test_config=None):
    CORS(app)
    app.url_map.strict_slashes = False
    initialize_app(app, test_config)

    # Handle the test route.
    @app.route('/test')
    def test_route():
        return 'Just testing the clusterDb server'

    return app


if __name__ == "__main__":
    create_app()
