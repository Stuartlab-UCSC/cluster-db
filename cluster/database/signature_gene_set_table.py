
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Signature_gene_set_table(Table):
    fields = [
        'name',
        'method',
        'clustering_solution_id'
    ]
    pass


signature_gene_set = Signature_gene_set_table()

