
# The base class for single table access.

from flask import current_app
from werkzeug.exceptions import abort
import logging, traceback, csv, sqlite3
from cluster.api.restplus import app_error, abort_if_json, abort_if_tsv, is_json, is_tsv
from cluster.database.db import get_db

log = logging.getLogger(__name__)

class Table(object):

    def _row_header_to_tsv(s, row):
        return '#' + s._row_to_tsv(row.keys())

    def _row_to_tsv(s, row):

        # Convert an sqlite row to a TSV line.
        tsv_row = str(row[0])
        for col in row[1:]:
            tsv_row += '\t' + str(col)
        return tsv_row

    def _rows_to_tsv(s, rows):

        # Convert sqlite rows to TSV lines.
        if len(rows) < 1:
            return ''

        # The header.
        tsv = s._row_header_to_tsv(rows[0])

        # The data rows.
        for row in rows:
            tsv += '\n' + s._row_to_tsv(row)
        return tsv

    def _rows_to_list_of_dicts(s, rows):

        # Convert sqlite rows to a list of dicts.
        list_of_dicts = []
        for row in rows:
            list_of_dicts.append(dict(row))
        return list_of_dicts

    def get_all_rows(s):

        # Return all rows as sqlite rows.
        db = get_db()
        cursor = db.execute('SELECT * FROM ' + s.table)
        return cursor.fetchall()

    def add(s, data):

        # Add one row.
        abort_if_tsv()
        db = get_db()

        # Find the foreign key ID by the foreign key name.
        fk_field, fk_id = s._get_foreign_key(db, data)
        if fk_field != None:
            data[fk_field] = fk_id

        try:
            cursor = s._add(data, db)
            db.commit()
        except Exception as e:
            trace = traceback.format_exc(100)
            log.error(trace)
            abort(400, str(trace))
        return {"id": cursor.lastrowid}

    def delete(s, name):
        try:
            row = s.get(name)
            print('delete:row:', row)
            if row == None:
                abort(404, 'Name not found: ' + str(name))
            db = get_db()
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()
        except sqlite3.IntegrityError as e:
            print ('delete sqlite3.IntegrityError:', str(e))
            trace = traceback.format_exc(100)
            log.error(trace)
            #raise Exception
            #raise app_error('This row is owned by another row connected by a foreign key')
            #abort(400, str(trace))
            abort(400, 'My custom message', custom='value')

        except Exception as e:
            print ('delete exception:', str(e))
            trace = traceback.format_exc(100)
            log.error(trace)
            abort(400, str(trace))
        return { 'id': row['id'] }

    def get(s, name=None):

        # Return one by name or return all rows.
        if name:

            # Return one row by ID.
            abort_if_tsv()
            row = get_db().execute(
                'SELECT * FROM ' + s.table + ' WHERE name = ?', (name,)).fetchone()
            if row is None:
                abort(404, 'Name not found: ' + str(name))
            return row

        # Return all as TSV.
        elif is_tsv():
            return s._rows_to_tsv(s.get_all_rows())

        # Return all rows as a list of dicts.
        return s._rows_to_list_of_dicts(s.get_all_rows())

    def load_tsv(name, file_path):

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
        abort_if_tsv()
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

