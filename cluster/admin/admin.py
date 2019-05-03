
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from cluster.auth.db_models import User, Role, UserRoles

class optsView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

class RoleView(optsView):
    form_columns = ['id', 'name']

class UserRolesView(optsView):
    can_create = False
    can_edit = False
    can_delete = False
    form_columns = ['role_id']

class UserView(optsView):
    can_create = False
    column_list = ('id', 'email', 'active', 'roles')
    def __str__(self):
        return self.name  # shows role names rather than IDs

def admin_init(app, db):
    admin = Admin(app, name='CellAtlas Admin', template_mode='bootstrap3')
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(UserRolesView(UserRoles, db.session))
