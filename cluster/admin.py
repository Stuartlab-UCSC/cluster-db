
# Admin mail and page functionality.
import os
from flask_user import current_user
from flask_admin.contrib.sqla import ModelView
from cluster.database.data_models import ClusterSolution, Dataset
from cluster.database.user_models import CellTypeWorksheet, Group, Role, User
from flask_admin import Admin
from flask_mail import Mail, Message

mail = None

# To add a batch action, perhaps to add many users to a role:
# https://flask-admin.readthedocs.io/en/latest/advanced/


def mail_admin(message, app):
    if current_user.is_authenticated:
        sender = current_user.email
        cc = current_user.email
    else:
        sender = 'unauthenticated@ucsc.edu'
        cc = None
    msg = Message('I wish that...', sender=sender, cc=cc,
        recipients=[app.config['MAIL_USERNAME']])
        #recipients=[os.environ.get("CLUSTERDB_EMAIL")])

    msg.body = message
    msg.html = '<p>' + message + '<p>'
    mail.send(msg)


def admin_routes(app):
    # Handle the test route.
    # Please leave this route for testing by the client.
    @app.route('/test')
    def test_route():
        return 'Just testing the clusterDb server'

    # Handle the mail-to-admin route.
    @app.route('/mail-admin/<string:message>')
    def mail_admin_route(message):
        mail_admin(message, app)
        return 'Mailed'


def init_app(app, db):
    admin = Admin(app, name='CellAtlas Admin', template_mode='bootstrap3')
    admin.add_view(CellTypeWorksheetView(CellTypeWorksheet, db.session))
    admin.add_view(ClusterSolutionView(ClusterSolution, db.session))
    admin.add_view(DatasetView(Dataset, db.session))
    admin.add_view(GroupView(Group, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(UserView(User, db.session))
    admin_routes(app)
    global mail
    mail = Mail(app)


class BaseView(ModelView):
    can_export = True
    column_default_sort = 'id'
    column_display_pk = True # display the primary key
    column_hide_backrefs = False
    # Only allow admins to look at these tables.
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_roles('admin')


class CellTypeWorksheetView(BaseView):

    list = ('id', 'place', 'name', 'user_id', 'expression_id', 'groups')
    column_filters = list
    column_list = list
    column_searchable_list = ('id', 'place', 'name', 'user_id', 'expression_id')


class ClusterSolutionView(BaseView):

    list = ('id', 'name', 'description', 'method',
        'method_implementation', 'method_url', 'method_parameters', 'scores',
        'analyst', 'likes', 'dataset_id')
    column_filters = list
    column_list = list
    column_searchable_list = list


class DatasetView(BaseView):

    list = ('id', 'name', 'uuid', 'species', 'organ',
        'cell_count', 'disease', 'platform', 'description', 'data_source_url',
         'publication_url')
    column_filters = list
    column_list = list
    column_searchable_list = list


class GroupView(BaseView):

    list = ('id', 'name', 'members', 'cellTypeWorksheets')
    column_filters = list
    column_list = list
    column_searchable_list = ('id', 'name')


class RoleView(BaseView):

    list = ('id', 'name', 'members')
    column_filters = list
    column_list = list
    column_searchable_list = ('id', 'name')


class UserView(BaseView):

    list = ('id', 'email', 'roles', 'groups', 'active', 'email_confirmed_at')
    can_create = False
    column_filters = list
    column_list = list
    column_searchable_list = ('id', 'email') #, 'roles')
    form_excluded_columns = ('email_confirmed_at', 'password')
    # form_widget_args to make username uneditable?
    form_widget_args = {
        'other_field': {
            'email': True
        }
    }

    def __str__(self):
        return self.name
