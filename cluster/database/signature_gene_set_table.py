
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution


class Signature_gene_table(Table):

    table = 'signature_gene_set'
    foreign_key_names = ['clustering_solution']

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO signature_gene_set (
                name,
                method,
                clustering_solution
            )
            VALUES (?,?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        row = clustering_solution._get_one(data['clustering_solution'])
        if row == None:
            return 'clustering_solution_id', None
        return 'clustering_solution_id', row['id']


signature_gene_set = Signature_gene_set_table()

