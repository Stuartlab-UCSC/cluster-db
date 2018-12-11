
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

    """
    def _get_vals(s, data, name=None):
        vals = []
        for key in data.keys():
            if not key in s.foreign_key_names:
            #if key != 'clustering':  # don't include the foreign key name
                vals.append(data[key])
        #if name != None:
        #    vals.append(name)
        return vals
    """

    """
    def _replace(s, name, data, db):
        db.execute('''
            UPDATE signature_gene_set SET
                name = ?,
                method = ?,
                clustering = ?
            WHERE name = ?
            ''', (s._get_vals(data, name))
        )
    """


signature_gene_set = Signature_gene_set_table()

