
from cluster.database.table import Table
from cluster.database.signature_gene_set_table import signature_gene_set


class Signature_gene_table(Table):

    table = 'signature_gene'
    parent_table = 'signature_gene_set'

    foreign_key_names = ['signature_gene_set']
    foreign_key_info = {
        'f_name_field': 'signature_gene_set',
        'f_key_field': 'signature_gene_set_id',
        'f_key_table': signature_gene_set
    }
    select_fields = 'name'

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO signature_gene (
                name,
                signature_gene_set_id
            )
            VALUES (?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        row = signature_gene_set._get_one(data['signature_gene_set'])
        if row == None:
            return 'signature_gene_set_id', None
        return 'signature_gene_set_id', row['id']


signature_gene = Signature_gene_table()

