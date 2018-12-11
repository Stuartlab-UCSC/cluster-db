
from cluster.database.table import Table
from cluster.database.datasetTable import dataset

class ClusteringTable(Table):

    table = 'clustering'

    def _add(s, data, db):
        cursor = db.execute(
            'INSERT INTO ' + s.table + ' ('
            ' name,'
            ' method,'
            ' method_implementation,'
            ' method_url,'
            ' method_parameters,'
            ' analyst,'
            ' secondary,'
            ' dataset_id)'
            ' VALUES (?,?,?,?,?,?,?,?)',
            s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        row = dataset._get_one(data['dataset'])
        if row == None:
            return 'dataset_id', None
        return 'dataset_id', row['id']


    def _get_vals(s, data, name=None):
        vals = [
            data['name'],
            data['method'],
            data['method_implementation'],
            data['method_url'],
            data['method_parameters'],
            data['analyst'],
            data['secondary'],
            data['dataset_id']
        ]
        if name != None:
            vals.append(name)
        return vals

    def _replace(s, name, data, db):
        db.execute(
            'UPDATE ' + s.table + ' SET'
            ' name = ?,'
            ' method = ?,'
            ' method_implementation = ?,'
            ' method_url = ?,'
            ' method_parameters = ?,'
            ' analyst = ?,'
            ' secondary = ?,'
            ' dataset_id = ?'
            ' WHERE name = ?',
            (s._get_vals(data, name))
        )


clustering = ClusteringTable()

