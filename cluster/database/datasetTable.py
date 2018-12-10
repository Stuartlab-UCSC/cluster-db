
from cluster.database.table import Table

class DatasetTable(Table):

    table = 'dataset'

    def _add(s, data, db):
        cursor = db.execute(
            'INSERT INTO ' + s.table + ' ('
            ' name,'
            ' species)'
            ' VALUES (?,?)',
            s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        return None, None

    def _get_vals(s, data, name=None):
        vals = [
            data['name'],
            data['species'],
        ]
        if name:
            vals.append(name)
        return vals

    def _replace(s, name, data, db):
        db.execute(
            'UPDATE ' + s.table + ' SET'
            ' name = ?,'
            ' species = ?'
            ' WHERE name = ?',
            (s._get_vals(data, name))
        )


dataset = DatasetTable()

