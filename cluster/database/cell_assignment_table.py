
from cluster.database.table import Table
from cluster.database.cluster_table import cluster
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.dataset_table import dataset
from cluster.database.db import get_db
import cluster.database.error as err
from cluster.database.error import Not_found, Not_found
import cluster.database.tsv as tsv


class Cluster_assignment_table(Table):
    def __init__(s):
        s.table = 'cluster_assignment'  # table name
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


cluster_assignment = Cluster_assignment_table()

