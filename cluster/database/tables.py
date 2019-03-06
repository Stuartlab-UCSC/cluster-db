"""
Provides access to database through sqlalchemy core objects (sqlalchemy.sql.schema.Table)
"""
from cluster.database.access import engine
from sqlalchemy import Table, MetaData

# Connection to the database.
metadata = MetaData()


dataset = Table('dataset', metadata, autoload=True, autoload_with=engine)


cluster_solution = Table('cluster_solution', metadata, autoload=True, autoload_with=engine)


cluster = Table('cluster', metadata, autoload=True, autoload_with=engine)


cell_assignment = Table('cell_of_cluster', metadata, autoload=True, autoload_with=engine)
