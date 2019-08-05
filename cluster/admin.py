
# Admin page functionality.

from flask_user import current_user
from flask_admin.contrib.sqla import ModelView
from cluster.database.data_models import ClusterSolution, Dataset
from cluster.database.user_models import User, Role
from flask_admin import Admin

# To add a batch action, perhaps to add many users to a role:
# https://flask-admin.readthedocs.io/en/latest/advanced/


def init_app(app, db):
    return
    admin = Admin(app, name='CellAtlas Admin', template_mode='bootstrap3')
    admin.add_view(ClusterSolutionView(ClusterSolution, db.session))
    admin.add_view(DatasetView(Dataset, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))


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


class RoleView(BaseView):

    list = ('id', 'name', 'members')
    column_filters = list
    column_list = list
    column_searchable_list = ('id', 'name')


class UserView(BaseView):

    list = ('id', 'email', 'roles', 'active', 'email_confirmed_at')
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
        return self.name  # shows role names rather than IDs