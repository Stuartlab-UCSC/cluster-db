import datetime
import logging.config
import os

from flask import Flask, Blueprint
from flask_babelex import Babel
from flask_cors import CORS
from flask_user import UserManager

from cluster.api.restplus import api
from cluster.database import db
from cluster.database.user_models import User

from cluster.api.user import ns as user_namespace
from cluster.api.sql import ns as sql_namespace
from cluster.api.cluster_solution import ns as cluster_solution_namespace
from cluster.api.dataset import ns as dataset_namespace
from cluster.api.marker import ns as marker_namespace
from cluster.api.dotplot import ns as dotplot_namespace

from cluster.database.user_models import CellTypeWorksheet, ExpCluster, ExpDimReduct, WorksheetUser, ClusterGeneTable, UserExpression

def initialize_blueprint(app):

    apiBlueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(apiBlueprint)

    api.add_namespace(cluster_solution_namespace)
    api.add_namespace(dataset_namespace)
    api.add_namespace(dotplot_namespace)
    api.add_namespace(marker_namespace)
    api.add_namespace(sql_namespace)
    api.add_namespace(user_namespace)

    app.register_blueprint(apiBlueprint)


def add_default_user(user_manager):

    user_already_there = User.query.filter(User.email == 'tester@test.com').first()
    if not user_already_there:
        user = User(
            id=1,
            email='tester@test.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('testT1234'),
        )

        db.session.add(user)
        db.session.commit()

    """
    user = user_already_there or user
    user_id = user.id

    ws_already_there = WorksheetUser.query.filter(WorksheetUser.user_id == user_id).first()
    
    if not ws_already_there:

        db.session.add(
            CellTypeWorksheet(
                id=1,
                name="test",
                place="cantfind"
            )
        )

        db.session.add(
            WorksheetUser(
                user_id=1,
                worksheet_id= 1
            )
        )

        from cluster.api.user import TEST_EXPRESSION_PICKLE_PATH, TEST_XY_PATH, TEST_CLUSTER_ID_PATH, TEST_MARKERS_DICT_PATH

        db.session.add(
            UserExpression(
                id=1,
                name="test",
                species="test",
                organ="test",
                place=TEST_EXPRESSION_PICKLE_PATH
            )
        )
        
        db.session.add(
            ExpDimReduct(
                name= "umap",
                place=TEST_XY_PATH,
                expression_id=1
            )
        )
        
        db.session.add(
            ExpCluster(
                id=1,
                name="lovain",
                place=TEST_CLUSTER_ID_PATH,
                expression_id=1
            )
        )
        
        db.session.add(
            ClusterGeneTable(
                cluster_id=1,
                place=TEST_MARKERS_DICT_PATH
            )
        )
       
        db.session.commit()

        """


def setup_logger(logfile='../logging.conf'):
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), logfile))
    logging.config.fileConfig(logging_conf_path)
    logging.getLogger(__name__)


def create_app(extra_config={}):

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    app.config.update(extra_config)

    testing = app.config["TESTING"]

    if not testing:
        setup_logger()

    CORS(app)
    Babel(app)

    app.url_map.strict_slashes = False
    initialize_blueprint(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        user_manager = UserManager(app, db, User)
        if not testing:
            add_default_user(user_manager)

    return app


if __name__ == "__main__":
    create_app()
