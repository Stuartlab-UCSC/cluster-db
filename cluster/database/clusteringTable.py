
from cluster.database.table import Table

class ClusteringTable(Table):

    table = 'clustering'

    def _getVals(s, data, id=None):
        vals = [
            data['name'],
            data['method'],
            data['method_url'],
            data['method_parameters'],
            data['analyst'],
            data['secondary'],
            data['dataset']
        ]
        if id:
            vals.append(id)
        return vals

    def _add(s, data, db):
        cursor = db.execute(
            'INSERT INTO ' + s.table + ' ('
            ' name,'
            ' method,'
            ' method_url,'
            ' method_parameters,'
            ' analyst,'
            ' secondary,'
            ' dataset)'
            ' VALUES (?,?,?,?,?,?,?)',
            s._getVals(data)
        )
        return cursor


clustering = ClusteringTable()

