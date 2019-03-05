
import os
from sqlalchemy import create_engine, Table, MetaData, select

# Connection to the database.
database_path = os.path.join(os.environ.get("CLUSTERDB"), "cluster.db")
engine = create_engine("sqlite:///%s" % database_path, echo=True)
metadata = MetaData()

# Accessor for each of the tables.
dataset = Table('dataset', metadata, autoload=True, autoload_with=engine)


cluster_solution = Table('cluster_solution', metadata, autoload=True, autoload_with=engine)


cluster = Table('cluster', metadata, autoload=True, autoload_with=engine)


cluster_assignment = Table('cell_of_cluster', metadata, autoload=True, autoload_with=engine)

# Common access functions
def one_dataset(dataset, datasetid, conn):
    select_stm = select([dataset]).where(dataset.c.id == datasetid)
    result = conn.execute(select_stm).fetchone()
    return result


def alldatasets(dataset, conn):
    """dataset is a sql alchemy core table, conn is engine.connect() obj
    Returns a list of dicts..."""
    select_stm = select([dataset.c.name, dataset.c.description, dataset.c.id])

    result = [dict(name=d[0], description=d[1], id=d[2]) for d in conn.execute(select_stm).fetchall()]
    return result


def cluster_solutions_per_dataset(cluster_solution, dataset, dataset_id, conn):
    """dataset and cluster* are core tables, dataset_id, engine.connect()
    returns a list of dicts"""
    select_stm = select([cluster_solution.c.name, cluster_solution.c.method, cluster_solution.c.id])\
        .select_from(dataset.join(cluster_solution))\
        .where(dataset.c.id == dataset_id)
    result = conn.execute(select_stm).fetchall()
    result = [dict(name=r[0], method=r[1], id=r[2]) for r in result]
    return result


def cellassignments(cell_of_cluster, cluster, cluster_solution_table, cluster_solution_id, conn):
    """
    returns list of dicts
    """
    select_stm = select([cell_of_cluster.c.name, cluster.c.name]).select_from(
          cluster_solution_table.join(cluster).join(cell_of_cluster)
        ).where(cluster_solution_table.c.id == cluster_solution_id)

    result = conn.execute(select_stm).fetchall()
    result = [dict(name=r[0], cluster_name=r[1]) for r in result]
    return result


def clustersolution(cluster_solution_table, clustersolid, conn):
    select_stm = select([cluster_solution_table.c.dataset_id]).where(cluster_solution_table.c.id == clustersolid)
    result = conn.execute(select_stm).fetchall()
    return result


def clusters(cluster_solution_table, clustersolid, cluster, conn):
    select_stm = select([cluster.c.name]).select_from(
          cluster_solution_table.join(cluster)
        ).where(cluster_solution_table.c.id == clustersolid)
    result = conn.execute(select_stm).fetchall()
    return result