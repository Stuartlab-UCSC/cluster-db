# app.py

import logging.config
import os
from cluster import settings
from flask import Flask, Blueprint
from flask_cors import CORS
from cluster.api.sql import ns as sql_namespace
from cluster.api.restplus import api
from cluster.api.user import ns as user_namespace
from cluster.database import db
from flask_security import SQLAlchemyUserDatastore
from cluster.database.user_models import User, Role
from flask_security import Security

from cluster.api.cluster_solution import ns as cluster_solution_namespace
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.marker import ns as marker_namespace
from cluster.api.dotplot import ns as dotplot_namespace


app = Flask(__name__)


logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
apiBlueprint = 0


def configure_app(flask_app, test_config):

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flask_app.config.from_mapping(
            RESTPLUS_VALIDATE= settings.RESTPLUS_VALIDATE,
            RESTPLUS_MASK_SWAGGER= settings.RESTPLUS_MASK_SWAGGER,
            DATABASE= settings.DATABASE, # for pre_sqlAlchemy.py
            SQLALCHEMY_DATABASE_URI="sqlite:///" + settings.DATABASE,
            SQLALCHEMY_BINDS={"users": "sqlite:///" + settings.USER_DATABASE},
            UPLOADS=settings.UPLOADS,
        )
        flask_app.config['SECRET_KEY'] = 'super-secret'
        flask_app.config['SECURITY_PASSWORD_SALT'] = 'super-secret'

    else:
        # load the test config if passed in
        flask_app.config.from_mapping(test_config)
        flask_app.config['DEBUG'] = False


def initialize_blueprint(flask_app):

    apiBlueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(apiBlueprint)

    api.add_namespace(cluster_solution_namespace)
    api.add_namespace(dataset_namespace)
    api.add_namespace(dotplot_namespace)
    api.add_namespace(marker_namespace)
    api.add_namespace(sql_namespace)
    api.add_namespace(user_namespace)

    flask_app.register_blueprint(apiBlueprint)


def initialize_app(flask_app, test_config):

    configure_app(flask_app, test_config)
    db.init_app(flask_app)
    initialize_blueprint(flask_app)

    with flask_app.app_context():
        db.create_all()
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        Security(app, user_datastore)


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
