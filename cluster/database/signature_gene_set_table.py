
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Signature_gene_set_table(Table):
    table = 'signature_gene_set'  # table name
    parentless_fields = [         # table fields minus row ID
        'name',
        'method',
    ]
    parentless_fields = parentless_fields
    fields = parentless_fields + ['clustering_solution_id']
    parent = {  # foreign keys in this table
        'field': 'clustering_solution',
        'table': clustering_solution
    }
    child_tables = [  # tables with foreign keys pointing to this table
        'signature_gene',
    ]
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


signature_gene_set = Signature_gene_set_table()

