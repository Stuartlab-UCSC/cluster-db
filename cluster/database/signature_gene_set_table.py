
from cluster.database.table import Table
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import get_db


class Signature_gene_set_table(Table):

    table = 'signature_gene_set'
    parent_table = 'clustering_solution'
    foreign_key_names = ['clustering_solution']
    foreign_key_info = {
        'f_name_field': 'clustering_solution',
        'f_key_field': 'clustering_solution_id',
        'f_key_table': clustering_solution
    }
    select_fields = 'name method'

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO signature_gene_set (
                name,
                method,
                clustering_solution_id
            )
            VALUES (?,?,?)
            ''', s._get_vals(data)
        )


signature_gene_set = Signature_gene_set_table()

