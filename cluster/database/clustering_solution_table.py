
from cluster.database.table import Table
from cluster.database.dataset_table import dataset


class Clustering_solution_table(Table):

    # Define some variables for this specialized table class.
    table = 'clustering_solution'  # table name
    tsv_header = [                # table fields minus row ID
        'name',
        'method',
        'method_implementation',
        'method_url',
        'method_parameters',
        'analyst',
        'secondary'
    ]
    base_fields = tsv_header
    fields = tsv_header + ['dataset_id']
    parent = {  # foreign keys in this table
        'field': 'dataset',
        'table': dataset
    }
    child_tables = [  # tables with foreign keys pointing to this table
        'signature_gene_set',
    ]
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


clustering_solution = Clustering_solution_table()

