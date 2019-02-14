
from cluster.database.table import Table
from cluster.database.dataset_table import dataset


class Clustering_solution_table(Table):

    def __init__(s):
        s.table = 'cluster_solution'  # table name
        s.parentless_fields = [          # table fields minus row ID
            'name',
            'method',
            'method_implementation',
            'method_url',
            'method_parameters',
            'scores',
            'analyst',
            'secondary'
        ]
        s.fields = s.parentless_fields + ['dataset_id']
        s.parent_table = ['dataset'] # ancestor tables of this table
        s.child_table = ['signature_gene_set', 'cluster']


cluster_solution = Clustering_solution_table()

