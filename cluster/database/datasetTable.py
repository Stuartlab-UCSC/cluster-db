
from cluster.database.table import Table

class DatasetTable(Table):

    table = 'dataset'

    def _getVals(s, data, id=None):
        vals = [
            data['name'],
            data['species'],
        ]
        if id:
            vals.append(id)
        return vals

    def _add(s, data, db):
        cursor = db.execute(
            'INSERT INTO ' + s.table + ' ('
            ' name,'
            ' species)'
            ' VALUES (?,?)',
            s._getVals(data)
        )
        return cursor

    def _replace(s, name, data, db):
        db.execute(
            'UPDATE ' + s.table + ' SET'
            ' name = ?,'
            ' species = ?'
            ' WHERE name = ?',
            (s._getVals(data, name))
        )


dataset = DatasetTable()

