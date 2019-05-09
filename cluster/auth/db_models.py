
# Provides access to authorization tables in the database.

from cluster.database import db
from cluster.database.access import engine
from sqlalchemy import Table, MetaData
from flask_user import UserMixin

# Define the User data-model.
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __bind_key__ = 'users' # use user db file rather than data db file
    
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    __bind_key__ = 'users' # use user db file rather than data db file
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name
        
# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    __bind_key__ = 'users' # use user db file rather than data db file
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
