
# The base class for single table access.

import logging, traceback, csv
from flask import current_app
from werkzeug.exceptions import abort
from cluster.api.restplus import abortIfJson, abortIfTsv, isJson, isTsv
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
        abortIfTsv()
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
        print('delete:row:', row)
        if row == None:
            abort(404, 'Name not found: ' + str(name))
        db = get_db()
        db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
        db.commit()
        return { 'id': row['id'] }

    def get(s, name=None):

        # Return one by name or return all rows.
        if name:

            # Return one row by ID.
            abortIfTsv()
            row = get_db().execute(
                'SELECT * FROM ' + s.table + ' WHERE name = ?', (name,)).fetchone()
            if row is None:
                abort(404, 'Name not found: ' + str(name))
            return row

        # Return all as TSV.
        elif isTsv():
            return s._rowsToTsv(s._getAllRows())

        # Return all rows as a list of dicts.
        return s._rowsToListOfDicts(s._getAllRows())

    def loadTsv(name, file_path):

        # Add rows from a TSV file to the table.
        # @param name: name of parent of new rows
        # @param file_path: TSV file path to load
        # @returns: row count or error, plus http code
        # TODO test that name exists
        try:
            db = get_db()
            with open(os.path(current_app.UPLOADS, file_path), 'r') as f:
                f = csv.reader(f, delimiter='\t')
                if not f.fieldnames == s._getFieldnames():
                    return { 'error': 'field name mismatch' }, 400
                try:
                    for row in f:
                        s._add(row.append(name), db)
                except:
                    return { 'error': 'load failed' }, 400
            db.commit()
        except:
            return { 'error': 'load failed, file not found' }, 404
        return { 'row_count': f.line_num }

    def update(s, name, field, value):
        abortIfTsv()
        try:
            row = dict(s.get(name))
            if row == None:
                abort(404, 'Name not found: ' + str(name))

            # Convert the value to the expected data type.
            # We only handle int, float, str.
            data_type = type(row[field]).__name__
            if data_type == 'int' or data_type == 'long':
                row[field] = int(value)
            elif data_type == 'float':
                row[field] = float(value)
            else:
                row[field] = value

            db = get_db()
            s._replace(name, row, db)
            db.commit()
        except:
            return { 'error': 'update failed' }, 400
        return { 'id': row['id'] }

