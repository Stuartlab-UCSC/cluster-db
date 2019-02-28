
from cluster.database_update.table import Table
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.dataset_table import dataset
from cluster.database.db import get_db
import cluster.database.error as err
from cluster.database.error import Not_found, Not_found
import cluster.database.tsv as tsv


class Cluster_assignment_table(Table):
    def __init__(s):
        s.table = 'cell_of_cluster'  # table name
        s.parentless_fields = [         # table fields minus IDs
            'name',
        ]
        s.fields = s.parentless_fields + ['cluster_id']
        s.tsv_fields = s.parentless_fields + ['cluster']
        s.parent_table = [ # ancestor tables of this table
            'cluster_solution',
            'dataset'
        ]
        s.cluster_table = cluster


cell_of_cluster = Cluster_assignment_table()

