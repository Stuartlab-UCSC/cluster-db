
from cluster.database.db import get_db


class TableBase(object):

    def _rowToTsv(s, row):

        # Convert an sqlite row to a TSV line.
        array = list(row)
        tsvRow = str(array[0])
        for col in array[1:]:
            tsvRow += '\t' + str(col)
        return tsvRow

    def _rowsToTsv(s, rows):

        # Convert sqlite rows to TSV lines.
        # TODO Should we use the standard csv library to write to a variable?
        if len(rows) < 1:
            return ''
        tsv = s._rowToTsv(rows[0])
        for row in rows[1:]:
            tsv += '\n' + s._rowToTsv(row)
        return tsv

    def _getAllRows(s):

        # Return all rows as sqlite rows.
        db = get_db()
        cursor = db.execute('SELECT * FROM ' + s.table)
        return cursor.fetchall()

    def add(s, data):

        # Add one row.
        db = get_db()
        try:
            s._add(data, db)
        except:
            return None
        db.commit()
        return data

    def delete(s, id):
        s.get(id)
        db = get_db()
        db.execute('DELETE FROM ' + s.table + ' WHERE id = ?', (id,))
        db.commit()

    def get(s, id=None):

        # Return one by ID or return all rows.
        if id:
            # Return one row by ID.
            row = get_db().execute(
                'SELECT * FROM ' + s.table + ' WHERE id = ?', (id,)).fetchone()

            return row

        # Return all rows as a list of dicts.
        return list(s._getAllRows())

    def getTsv(s):

        # Return all rows as a TSV-formatted string.
        return s._rowsToTsv(s._getAllRows())

    def update(s, id, data):
        row = s.get(id)
        if row == None:
            return None

        db = get_db()
        try:
            s._update(id, data, db)
        except:
            return None
        db.commit()
        return data

