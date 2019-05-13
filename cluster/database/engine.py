"""
Supplies an engine to access sql
"""
import os
from sqlalchemy import create_engine

# Connection to the database.
database_path = os.path.join(os.environ.get("CLUSTERDB"), "cluster.db")
engine = create_engine("sqlite:///%s" % database_path, echo=False)
