
from cluster.database.table import Table
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.db import get_db


class Signature_gene_table(Table):
    table = 'signature_gene'  # table name
    parentless_fields = [         # table fields minus row ID
        'name',
    ]
    fields = parentless_fields + ['signature_gene_set_id']
    tsv_header = parentless_fields + ['signature_gene_set']
    parent = {  # foreign keys in this table
        'field': 'signature_gene_set',
        'table': signature_gene_set
    }
    # The 'insert into database' string.
    # This is duplicated in each specialized table class
    # because it is built at class instance creation.
    add_one_string = \
        'INSERT INTO ' + table + ' (' + \
        ','.join(fields) + \
        ')' + \
        'VALUES (' + ('?,' * len(fields))[:-1] + ')'


signature_gene = Signature_gene_table()

