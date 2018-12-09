
from cluster.database.table import Table

class ClusteringTable(Table):

    table = 'clustering'

    def _getVals(s, data, name=None):
        vals = [
            data['name'],
            data['method'],
            data['method_implementation'],
            data['method_url'],
            data['method_parameters'],
            data['analyst'],
            data['secondary'],
            data['dataset']
        ]
        if name != None:
            vals.append(name)
        return vals

    def _add(s, data, db):
        vals = s._getVals(data)
        print('vals:', vals)
        cursor = db.execute(
            'INSERT INTO ' + s.table + ' ('
            ' name,'
            ' method,'
            ' method_implementation,'
            ' method_url,'
            ' method_parameters,'
            ' analyst,'
            ' secondary,'
            ' dataset)'
            ' VALUES (?,?,?,?,?,?,?,?)',
            s._getVals(data)
        )
        return cursor

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
            ' dataset = ?'
            ' WHERE name = ?',
            (s._getVals(data, name))
        )


clustering = ClusteringTable()

