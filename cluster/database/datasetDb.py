
from cluster.database.db import get_db
from cluster.database.tableBase import TableBase


class DatasetTable(TableBase):

    table = 'dataset'

    def _add(s, data, db):
         db.execute(
            'INSERT INTO ' + s.table +
            ' (id, detail)'
            ' VALUES (?,?)',
            (data['id'], data['detail'],)
        )

    def _update(s, id, data, db):
        db.execute(
            'UPDATE ' + s.table +
            ' SET id = ?, detail = ?'
            ' WHERE id = ?',
            (data['id'], data['detail'], data['id'],)
        )


dataset = DatasetTable()

