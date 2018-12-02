
from cluster.database.db import get_db


class Dataset(object):

    def addOne(s, data):

        # Add one row.
        db = get_db()
        db.execute(
            'INSERT INTO dataset (id, detail)'
            ' VALUES (?,?)',
            (data['id'], data['detail'])
        )
        db.commit()
        return data

    def _rowsToArrays(s, rows):

        # Convert sqlite rows to a 2D array.
        arr = []
        for row in rows:
            for col in row:
                arr.append(list(row))
        return arr

    def _rowToTsv(s, row):

        # Convert an sqlite row to a TSV line.
        array = list(row)
        tsvRow = str(array[0])
        for col in array[1:]:
            tsvRow += '\t' + str(col)
        return tsvRow

    def _rowsToTsv(s, rows):

        # Convert a sqlite rows to TSV lines.
        tsv = s._rowToTsv(rows[0])
        for row in rows[1:]:
            tsv += '\n' + s._rowToTsv(row)
        return tsv

    def getAll(s, file=None):

        # Get all rows that are in the table.
        # @returns: an array of table rows in an object if not written to file
        db = get_db()
        cursor = db.execute('SELECT * FROM dataset')
        rows = cursor.fetchall()
        tsv = s._rowsToTsv(rows)
        return tsv

dataset = Dataset()

