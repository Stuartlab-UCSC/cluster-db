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


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class CellTypeWorksheet(SurrogatePK, db.Model):
    __tablename__ = "worksheet"
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)


class WorksheetUser(SurrogatePK, db.Model):
    __tablename__ = "worksheetuser"
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    worksheet_id = db.Column(db.Integer(), db.ForeignKey('worksheet.id'))


class WorksheetRole(SurrogatePK):
    __tablename__ = "worksheetrole"
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    worksheet_id = db.Column(db.Integer(), db.ForeignKey('worksheet.id'))


class DsDimReduct(SurrogatePK, db.Model):
    # Multiple dim reducts per dataset.
    __tablename__ = "dsdimreduct"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class DsCluster(SurrogatePK, db.Model):
    __tablename__ = "dscluster"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class ClusterGeneTable(SurrogatePK, db.Model):
    __table_name__= "clustergenetable"
    place = Column(String, nullable=False)
    cluster_id = Column(Integer, ForeignKey("dscluster.id"), nullable=False)


class UserDataset(SurrogatePK):
    __tablename__ = "userdataset"
    species = Column(String, nullable=True)
    organ = Column(String, nullable=True)
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)