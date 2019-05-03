
# flask-user templates
# https://flask-user.readthedocs.io/en/latest/unused.html#customizingformtemplates

from flask_user import UserManager
from cluster.auth.db_models import Role, User


def default_auth_accounts(app, db):

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
            #active
            #last_active
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            traceback.print_exc()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()
