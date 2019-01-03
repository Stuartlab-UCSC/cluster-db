
from cluster.database.table import Table
from cluster.database.dataset_table import dataset


class Clustering_solution_table(Table):

    table = 'clustering_solution'
    parent_table = 'dataset'

    foreign_key_names = ['dataset']
    foreign_key_info = {
        'f_name_field': 'dataset',
        'f_key_field': 'dataset_id',
        'f_key_table': dataset
    }
    select_fields = \
        'name ' + \
        'method ' + \
        'method_implementation ' + \
        'method_url ' + \
        'method_parameters ' + \
        'analyst ' + \
        'secondary'

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


clustering_solution = Clustering_solution_table()

