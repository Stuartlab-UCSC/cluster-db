from cluster.database import db, SurrogatePK
from flask_user import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')


    roles = db.relationship('Role', secondary="user_roles",
                            backref=db.backref('users', lazy='dynamic'))

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class CellTypeWorksheet(SurrogatePK, db.Model):
    __tablename__ = "worksheet"
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)
    @classmethod
    def get_by_name(cls, record_name):
        """Get record by ID."""
        if isinstance(record_name, str)   :
            return cls.query.filter(cls.name == record_name).first()


class WorksheetUser(SurrogatePK, db.Model):
    __tablename__ = "worksheetuser"
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    worksheet_id = db.Column(db.Integer(), db.ForeignKey('worksheet.id'))

    @classmethod
    def get_user_worksheets(cls, user_id):

        return cls.query.filter(cls.user_id == user_id)


class UserExpression(SurrogatePK, db.Model):
    __tablename__ = "userexpression"
    species = Column(String, nullable=True)
    organ = Column(String, nullable=True)
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)


class WorksheetRole(SurrogatePK, db.Model):
    __tablename__ = "worksheetrole"
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    worksheet_id = db.Column(db.Integer(), db.ForeignKey('worksheet.id'))


class ExpDimReduct(SurrogatePK, db.Model):
    # Multiple dim reducts per dataset.
    __tablename__ = "dsdimreduct"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    expression_id = Column(Integer, ForeignKey("userexpression.id"), nullable=False)


class ExpCluster(SurrogatePK, db.Model):
    __tablename__ = "expcluster"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    expression_id = Column(Integer, ForeignKey("userexpression.id"), nullable=False)


class ClusterGeneTable(SurrogatePK, db.Model):
    __table_name__= "clustergenetable"
    place = Column(String, nullable=False)
    cluster_id = Column(Integer, ForeignKey("expcluster.id"), nullable=False)


