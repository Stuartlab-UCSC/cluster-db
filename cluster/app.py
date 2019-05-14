# app.py

import logging.config
import os
from cluster.settings import Settings
from flask import Flask, Blueprint
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
from cluster.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
adminManager = 0
apiBlueprint = 0
userManager = 0


def configure_app(flask_app, test_config):
    if test_config is None:
        flask_app.config.from_object(Settings)
        flask_app.config.from_object(AuthConfigClass)
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///" + flask_app.config['DATABASE']
        flask_app.config['SQLALCHEMY_BINDS'] = \
            {"users": "sqlite:///" + flask_app.config['USER_DATABASE']}
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

    apiBlueprint = flask_app.register_blueprint(apiBlueprint)


def initialize_app(flask_app, test_config):
    configure_app(flask_app, test_config)
    db.init_app(flask_app)
    Babel(flask_app) # for auth at least
    initialize_blueprint(flask_app)
    global adminManager
    if (not adminManager):
        adminManager = Admin(flask_app, name='CellAtlas Admin', template_mode='bootstrap3')
        admin_init(db, adminManager)
    
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
