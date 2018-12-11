
from cluster.database.table import Table

class DatasetTable(Table):

    table = 'dataset'

    def _add(s, data, db):
        cursor = db.execute('''
            INSERT INTO dataset (
                name,
                species
            )
            VALUES (?,?)
            ''', s._get_vals(data)
        )
        return cursor

    def _get_foreign_key(s, db, data):
        return None, None

    def _get_vals(s, data, name=None):
        vals = [
            data['name'],
            data['species'],
        ]
        """
        # The flask_restplus model guarantees the order in the dict.
        vals = []
        for key in data.keys():
            vals.append(data[key])
        """
        if name != None:
            vals.append(name)
        return vals

    def _replace(s, name, data, db):
        db.execute('''
            UPDATE dataset SET
                name = ?,
                species = ?
            WHERE name = ?
            ''', (s._get_vals(data, name))
        )


dataset = DatasetTable()

