
from cluster.database_update.table import Table


class Dataset_table(Table):

    def __init__(s):
        # Define some variables for this specialized table class.
        s.table = 'dataset'      # table name
        s.parentless_fields = [  # table fields minus parent IDs
            'name',
            'uuid',
            'species',
            'organ',
            'cell_count',
            'disease',
            'platform',
            'description',
            'data_source_url',
            'publication_url',
        ]
        s.fields = s.parentless_fields
        s.parent_table = None  # ancestor tables of this table
        s.child_table = ['cluster_solution']

# The table instance.
dataset = Dataset_table()

