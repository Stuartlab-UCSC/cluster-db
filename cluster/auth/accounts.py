
# flask-user templates
"""
import datetime
from flask_user import UserManager
from cluster.auth.db_models import Role, User


def default_auth_accounts(app, db):
    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)
    
    # Create initial test admin@example.com with 'admin' role.
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='admin'))
        db.session.add(user)
        db.session.commit()
"""
