
from cluster.database.table import Table


class Dataset_table(Table):

    # Define some variables for this specialized table class.
    table = 'dataset'      # table name
    parentless_fields = [  # table fields minus parent IDs
        'name',
        'species',
    ]
    fields = parentless_fields
    tsv_header = fields
    child_tables = [   # tables with foreign keys pointing to this table
        'clustering_solution'
    ]
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


# The table instance.
dataset = Dataset_table()

