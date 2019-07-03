from cluster.database import Model, SurrogatePK, backref, relationship
from flask_user import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Role(Model):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    active = Column('is_active', Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = Column(String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = Column(DateTime())
    password = Column(String(255), nullable=False, server_default='')

    # User information
    first_name = Column(String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = Column(String(100, collation='NOCASE'), nullable=False, server_default='')


    roles = relationship('Role', secondary="user_roles",
                            backref=backref('users', lazy='dynamic'))

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()


class UserRoles(Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('role.id', ondelete='CASCADE'))


class CellTypeWorksheet(SurrogatePK, Model):
    __tablename__ = "worksheet"
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)
    @classmethod
    def get_by_name(cls, record_name):
        if isinstance(record_name, str):
            return cls.query.filter(cls.name == record_name).first()


class WorksheetUser(SurrogatePK, Model):
    __tablename__ = "worksheetuser"
    user_id = Column(Integer(), ForeignKey('user.id'))
    worksheet_id = Column(Integer(), ForeignKey('worksheet.id'))

    @classmethod
    def get_user_worksheets(cls, user_id):
        return cls.query.filter(cls.user_id == user_id)


    @classmethod
    def get_worksheet(cls, user, worksheet_name):
        user_ws = cls.get_user_worksheets(user.id).filter(CellTypeWorksheet.name == worksheet_name).first()
        try:
            worksheet = CellTypeWorksheet.get_by_id(user_ws.worksheet_id)
        except AttributeError:
            raise ValueError("The user has no worksheet of the given name.")

        return worksheet


class UserExpression(SurrogatePK, Model):
    __tablename__ = "userexpression"
    species = Column(String, nullable=True)
    organ = Column(String, nullable=True)
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)
    worksheet_id = Column(Integer(), ForeignKey('worksheet.id'), unique=True)

    @classmethod
    def get_by_worksheet(cls, worksheet):
        return UserExpression.query.filter(UserExpression.worksheet_id == worksheet.id).one()


class WorksheetRole(SurrogatePK, Model):
    __tablename__ = "worksheetrole"
    role_id = Column(Integer(), ForeignKey('role.id'))
    worksheet_id = Column(Integer(), ForeignKey('worksheet.id'))


class ExpDimReduct(SurrogatePK, Model):
    # Multiple dim reducts per dataset.
    __tablename__ = "dsdimreduct"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    expression_id = Column(Integer, ForeignKey("userexpression.id"), nullable=False)

    @classmethod
    def get_by_expression(cls, expression):
        return cls.query.filter(cls.expression_id == expression.id).first()

class ExpCluster(SurrogatePK, Model):
    __tablename__ = "expcluster"
    name = Column(String, nullable=False)
    place = Column(String, nullable=False)
    expression_id = Column(Integer, ForeignKey("userexpression.id"), nullable=False)

    @classmethod
    def get_cluster(cls, expression):
        return cls.query.filter(cls.expression_id == expression.id).one()


class ClusterGeneTable(SurrogatePK, Model):
    __table_name__= "clustergenetable"
    place = Column(String, nullable=False)
    cluster_id = Column(Integer, ForeignKey("expcluster.id"), nullable=False)

    @classmethod
    def get_table(cls, cluster):
        return cls.query.filter(cls.cluster_id == cluster.id).first()

