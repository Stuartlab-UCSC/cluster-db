
# flask-user templates
import datetime
from flask_user import UserManager
from cluster.auth.db_models import Role, User


def auth_temporary_account(app, db, user_manager):
    # Setup Flask-User and specify the User data-model
    
    # Create initial test admin@replace.me with 'admin' role.
    if not User.query.filter(User.email == 'admin@replace.me').first():
        user = User(
            email='admin@replace.me',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='admin'))
        db.session.add(user)
        # Sometimes timing is such that account attempts to be created twice.
        try:
            db.session.commit()
        except:
            pass
