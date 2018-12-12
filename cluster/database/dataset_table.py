
from cluster.database.table import Table

class DatasetTable(Table):

    table = 'dataset'
    foreign_key_names = []

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

    # TODO: use Table class function after getting all fields in.
    def _get_vals(s, data, name=None):
        vals = [
            data['name'],
            data['species'],
        ]
        if name != None:
            vals.append(name)
        return vals


dataset = DatasetTable()

