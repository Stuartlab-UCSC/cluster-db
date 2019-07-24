from cluster.database import Model, SurrogatePK, backref, relationship
from flask_user import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from cluster.database.filename_constants import XYS, EXPRESSION, CLUSTERING, MARKER_TABLE, STATE
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm.exc import NoResultFound
import os


class Role(Model):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    members = relationship('User', secondary='user_roles')


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
        return cls.query.filter(cls.email == email).one()


class UserRoles(Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('role.id', ondelete='CASCADE'))


class CellTypeWorksheet(SurrogatePK, Model):
    __tablename__ = "worksheet"
    id = Column(Integer(), primary_key=True)
    name = Column(String)
    place = Column(String)
    user_id = Column(Integer(), ForeignKey('user.id'))
    expression_id = Column(Integer(), ForeignKey('userexpression.id'))
    __table_args__ = (UniqueConstraint('name', 'user_id', name="ws:user"),)


    @classmethod
    def get_user_worksheets(cls, user):
        return cls.query.filter(cls.user_id == user.id)

    @classmethod
    def get_user_worksheet_names(cls, user):
        return [ws.name for ws in cls.get_user_worksheets(user)]

    @classmethod
    def get_worksheet(cls, user, worksheet_name):
        user_ws = cls.get_user_worksheets(user).filter(cls.name == worksheet_name).one()
        not_found = user_ws is None
        if not_found:
            return None

        return user_ws


class UserExpression(SurrogatePK, Model):
    __tablename__ = "userexpression"
    id = Column(Integer(), primary_key=True)
    species = Column(String, nullable=True)
    organ = Column(String, nullable=True)
    name = Column(String, nullable=True)
    place = Column(String, nullable=True)

    @classmethod
    def get_by_worksheet(cls, worksheet):
        return UserExpression.query.filter(UserExpression.id == worksheet.expression_id).one()


class WorksheetRole(SurrogatePK, Model):
    __tablename__ = "worksheetrole"
    id = Column(Integer(), primary_key=True)
    role_id = Column(Integer(), ForeignKey('role.id'))
    worksheet_id = Column(Integer(), ForeignKey('worksheet.id'))


class ExpDimReduct(SurrogatePK, Model):
    __tablename__ = "dsdimreduct"
    id = Column(Integer(), primary_key=True)
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
    id = Column(Integer(), primary_key=True)
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


def get_all_worksheet_paths(user_email, worksheet_name):
    user = User.get_by_email(user_email)
    try:
        ws = CellTypeWorksheet.get_worksheet(user, worksheet_name)

    except NoResultFound:
        return None

    user_exp = UserExpression.get_by_worksheet(ws)
    clustering = ExpCluster.get_cluster(user_exp)  # assumes ther is only one...
    marker_table = ClusterGeneTable.get_table(clustering)
    reduction = ExpDimReduct.get_by_expression(user_exp)  # assumes there is only one ...

    return {
        XYS: reduction.place,
        STATE: ws.place,
        EXPRESSION: user_exp.place,
        CLUSTERING: clustering.place,
        MARKER_TABLE: marker_table.place,
    }


def add_worksheet_entries(
        session,
        user_email,
        worksheet_name,
        organ=None,
        species=None,
        dataset_name=None,
        cluster_name=None,
):
    """
    Single api for the tables needed to have a worksheet.
    :param session:
    :param worksheet_name:
    :param worksheet_path:
    :param user_id:
    :param exp_data_path:
    :param cluster_path:
    :param reductions:
    :param organ:
    :param species:
    :param dataset_name:
    :param cluster_name:
    :return:
    """

    try:
        CellTypeWorksheet.get_worksheet(User.get_by_email(user_email), worksheet_name)

    except NoResultFound:
        print("adding entry worksheet entry", user_email, worksheet_name)

        worksheet_root = os.path.join(user_email, worksheet_name)
        worksheet_path = os.path.join(worksheet_root, STATE)
        exp_data_path  = os.path.join(worksheet_root, EXPRESSION)
        cluster_path = os.path.join(worksheet_root, CLUSTERING)
        xys_path = os.path.join(worksheet_root, XYS)
        marker_path = os.path.join(worksheet_root, MARKER_TABLE)

        user_id = User.get_by_email(user_email).id

        user_exp = UserExpression(
            species=species,
            organ=organ,
            name=dataset_name,
            place=exp_data_path,
        )

        session.add(user_exp)
        session.commit()

        ws = CellTypeWorksheet(
            name=worksheet_name,
            place=worksheet_path,
            user_id=user_id,
            expression_id=user_exp.id
        )

        session.add(ws)
        session.commit()

        reduct = ExpDimReduct(
            name="xys",
            expression_id=user_exp.id,
            place=xys_path
        )
        session.add(reduct)
        session.commit()


        cluster = ExpCluster(
            name=cluster_name,
            expression_id=user_exp.id,
            place=cluster_path
        )

        session.add(cluster)
        session.commit()


        marker_table = ClusterGeneTable(
            place=marker_path,
            cluster_id=cluster.id
        )

        session.add(marker_table)
        session.commit()
