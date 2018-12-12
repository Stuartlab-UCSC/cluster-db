
from cluster.database.table import Table
from cluster.database.clustering_table import clustering


class Signature_gene_table(Table):

    table = 'signature_gene_set'
    foreign_key_names = ['clustering']

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO signature_gene_set (
                name,
                method,
                clustering
            )
            VALUES (?,?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        row = clustering._get_one(data['clustering'])
        if row == None:
            return 'clustering_id', None
        return 'clustering_id', row['id']


signature_gene_set = Signature_gene_set_table()

