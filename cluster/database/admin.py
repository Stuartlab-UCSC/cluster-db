
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from cluster.database import db
from cluster.database.models import Dataset

def init_admin(app):
    # set optional bootswatch theme
    #app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='cellAtlas', template_mode='bootstrap3')
    # Add administrative views here

    #admin.add_view(ModelView(Dataset, db.session))
