"""
Supplies an engine to access sql, and common data access functions.

The tables required by these functions are found in cluster.database.tables
"""
import os
from sqlalchemy import select, and_



def one_dataset(dataset_table, dataset_table_id, conn):
    """
    Return one data set from the data sets table with a data set id.
    :param dataset_table: (sqlalchemy.sql.schema.Table)
    :param dataset_table_id: (int)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: tuple representation of the data set table schema.
    """
    select_stm = select([dataset_table]).where(dataset_table.c.id == dataset_table_id)
    result = conn.execute(select_stm).fetchone()
    return result



def all_datasets(dataset_table, conn):
    """
    Return all data sets from the data set table.
    :param dataset_table: (sqlalchemy.sql.schema.Table)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: a list of dictionaries {name: (string), description: (string), id: (int) }
    """
    select_stm = select([dataset_table.c.name, dataset_table.c.description, dataset_table.c.id])

    result = [dict(name=d[0], description=d[1], id=d[2]) for d in conn.execute(select_stm).fetchall()]
    return result


def cluster_solutions(cs_table, dataset_table, dataset_table_id, conn):
    """
    Return all cluster solutions available for a given data set id.
    :param cs_table: (sqlalchemy.sql.schema.Table) cluster solutions
    :param dataset_table: (sqlalchemy.sql.schema.Table)
    :param dataset_table_id: (int)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: a list of dictionaries {name: (string), method: (string), id: (int) }
    """
    select_stm = select([cs_table.c.name, cs_table.c.method, cs_table.c.id])\
        .select_from(dataset_table.join(cs_table))\
        .where(dataset_table.c.id == dataset_table_id)
    result = conn.execute(select_stm).fetchall()
    result = [dict(name=r[0], method=r[1], id=r[2]) for r in result]
    return result


def cell_assignments(ca_table, cluster_table, cs_table, cluster_solution_id, conn):
    """
    Return all cell assignments to clusters for a given cluster solution id.
    :param ca_table: (sqlalchemy.sql.schema.Table) cell assignments table
    :param cluster_table: (sqlalchemy.sql.schema.Table) 
    :param cs_table: (sqlalchemy.sql.schema.Table) cluster solution table
    :param cluster_solution_id: (int)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: list of dictionaries {name: string, cluster_name: string}
    """
    select_stm = select([ca_table.c.name, cluster_table.c.name]).select_from(
          cs_table.join(cluster_table).join(ca_table)
        ).where(cs_table.c.id == cluster_solution_id)

    result = conn.execute(select_stm).fetchall()
    result = [dict(name=r[0], cluster_name=r[1]) for r in result]
    return result



def one_cluster_solution(cs_table, cluster_solution_id, conn):
    """
    Return a clustering solution with a given cluster solution id.
    :param cs_table: (sqlalchemy.sql.schema.Table) cluster solutions
    :param cluster_solution_id: (int)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: list of tuples only containing data set id the cluster belongs to.
    """
    select_stm = select([cs_table.c.dataset_id]).where(cs_table.c.id == cluster_solution_id)
    result = conn.execute(select_stm).fetchall()
    return result


def cluster_solution_id(dataset_table, dataset_name, cluster_solution_table, cluster_solution_name, conn):
    """

    :param dataset_table:
    :param dataset_name:
    :param cluster_solution_table:
    :param cluster_solution_name:
    :return:
    """
    select_stm = select([cluster_solution_table.c.id, dataset_table.c.id]).where(
        and_(
            cluster_solution_table.c.name == cluster_solution_name,
            dataset_table.c.name == dataset_name
        )

    )
    cs_id = conn.execute(select_stm).fetchone()[0]
    return cs_id


def clusters(cs_table, cluster_solution_id, cluster_table, conn):
    """
    Return all the clusters from a given cluster solution id
    :param cs_table: (sqlalchemy.sql.schema.Table) cluster solutions
    :param cluster_solution_id: (int)
    :param cluster_table: (sqlalchemy.sql.schema.Table)
    :param conn: (sqlalchemy.engine.base.Connection)
    :return: list of tuples only containing the cluster name
    """
    select_stm = select([cluster_table.c.name]).select_from(
          cs_table.join(cluster_table)
        ).where(cs_table.c.id == cluster_solution_id)
    result = conn.execute(select_stm).fetchall()
    return result
