
# flask-user templates
import datetime
from flask import redirect
from flask_user import UserManager
from cluster.auth.db_models import Role, User
from cluster.auth.routes import auth_routes

userManager = 0
# The view server URL to redirect at the end of auth processing.
viewer_url = 0

def auth_temporary_account(app, db):
    # Setup Flask-User and specify the User data-model
    
    # Create initial test admin@replace.me with 'admin' role.
    if not User.query.filter(User.email == 'admin@replace.me').first():
        user = User(
            email='admin@replace.me',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=userManager.hash_password('Password1'),
        )
        user.roles.append(Role(name='admin'))
        db.session.add(user)
        # Sometimes timing is such that account attempts to be created twice.
        try:
            db.session.commit()
        except:
            pass


def unauthorized_view(Resource):
    return ('403', 403)


def auth_accounts_init(app, db):
    global viewer_url
    viewer_url = app.config['VIEWER_URL'] + 'auth'
    global userManager
    if (not userManager):
        userManager = UserManager(app, db, User)
        auth_temporary_account(app, db)
        auth_routes(app, db)

