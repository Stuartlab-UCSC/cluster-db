
from cluster.database.table import Table
from cluster.database.dataset_table import dataset

class ClusteringTable(Table):

    table = 'clustering'

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO clustering (
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


    def _get_vals(s, data, name=None):

        # The flask_restplus model guarantees the order in the dict.
        vals = []
        for key in data.keys():
            if key != 'dataset':  # don't include the dataset name
                vals.append(data[key])

        if name != None:
            vals.append(name)
        return vals

    def _replace(s, name, data, db):
        db.execute('''
            UPDATE clustering SET
                name = ?,
                method = ?,
                method_implementation = ?,
                method_url = ?,
                method_parameters = ?,
                analyst = ?,
                secondary = ?,
                dataset_id = ?
            WHERE name = ?
            ''', (s._get_vals(data, name))
        )


clustering = ClusteringTable()

