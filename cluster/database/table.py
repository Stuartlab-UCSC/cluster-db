
# The base class for single table access.

import logging, traceback
from werkzeug.exceptions import abort
from cluster.database.db import get_db

log = logging.getLogger(__name__)

class Table(object):

    def _rowHeaderToTsv(s, row):
        return '#' + s._rowToTsv(row.keys())

    def _rowToTsv(s, row):

        # Convert an sqlite row to a TSV line.
        tsvRow = str(row[0])
        for col in row[1:]:
            tsvRow += '\t' + str(col)
        return tsvRow

    def _rowsToTsv(s, rows):

        # Convert sqlite rows to TSV lines.
        if len(rows) < 1:
            return ''

        # The header.
        tsv = s._rowHeaderToTsv(rows[0])

        # The data rows.
        for row in rows:
            tsv += '\n' + s._rowToTsv(row)
        return tsv

    def _rowsToListOfDicts(s, rows):

        # Convert sqlite rows to a list of dicts.
        listOfDicts = []
        for row in rows:
            listOfDicts.append(dict(row))
        return listOfDicts

    def _getAllRows(s):

        # Return all rows as sqlite rows.
        db = get_db()
        cursor = db.execute('SELECT * FROM ' + s.table)
        return cursor.fetchall()

    def add(s, data):

        # Add one row.
        db = get_db()
        try:
            cursor = s._add(data, db)
            db.commit()
        except Exception as e:
            trace = traceback.format_exc(100)
            log.error(trace)
            abort(400, str(trace))
        return {"id": cursor.lastrowid}

    def delete(s, name):
        row = s.get(name)
        if row == None:
            return None
        db = get_db()
        db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
        db.commit()
        return { 'id': row['id'] }

    def replace(s, name, data):
        row = s.get(name)
        if row == None:
            return None
        db = get_db()
        s._replace(name, data, db)
        db.commit()
        return { 'id': row['id'] }

    def get(s, name=None):

        # Return one by name or return all rows.
        if name:
            # Return one row by ID.
            row = get_db().execute(
                'SELECT * FROM ' + s.table + ' WHERE name = ?', (name,)).fetchone()
            return row

        # Return all rows as a list of dicts.
        return s._rowsToListOfDicts(s._getAllRows())

    def getTsv(s):

        # Return all rows as a TSV-formatted string.
        print('in getTsv()')
        return s._rowsToTsv(s._getAllRows())

    def _deleteAll(s):

        # Clear the table of all data, usually to reload the table.
        # @returns: nothing
        get_db().execute('DELETE FROM ' + s.table)

    def tsvAddManyFromFile(s, filePath, replace=False):

        # Add many rows from a file to the table.
        # @param filePath: the full path to the TSV file
        # @param replace: True to replace all rows, False to append
        # @returns: 0 on success, 1 on failue
        if replace:
            s._deleteAll()
        db = get_db()
        with open(filePath, 'r') as f:
            f = csv.reader(f, delimiter='\t')
            try:
                for row in f:
                    s._add(row, db)
            except:
                return 1
        db.commit()
        return 0
