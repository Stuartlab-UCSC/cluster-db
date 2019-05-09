
# Admin page functionality.

from flask_user import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from cluster.auth.db_models import User, Role

# To add a batch action, perhaps to add many users to a role:
# https://flask-admin.readthedocs.io/en/latest/advanced/

class BaseView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_roles('admin')

class RoleView(BaseView):
    form_columns = ['id', 'name']
    form_excluded_columns = ['id']

class UserView(BaseView):
    can_create = False
    column_list = ('id', 'email', 'active', 'roles')
    form_excluded_columns = ['email', 'email_confirmed_at', 'password']
    def __str__(self):
        return self.name  # shows role names rather than IDs

def admin_init(app, db):
    admin = Admin(app, name='CellAtlas Admin', template_mode='bootstrap3')
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
