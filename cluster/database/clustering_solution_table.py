
from cluster.database.table import Table
from cluster.database.dataset_table import dataset

class Clustering_solution_table(Table):

    table = 'clustering_solution'
    foreign_key_names = ['dataset']

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO clustering_solution (
                name,
                method,
                method_implementation,
                method_url,
                method_parameters,
                analyst,
                secondary,
                dataset_id
            )
            VALUES (?,?,?, ?,?,?, ?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        row = dataset._get_one(data['dataset'])
        if row == None:
            return 'dataset_id', None
        return 'dataset_id', row['id']


clustering_solution = Clustering_solution_table()

