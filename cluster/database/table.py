
# The base class for single table access.

from flask import current_app
from flask_restplus import abort
import csv, sqlite3
from cluster.api.restplus import exception_if_tsv, is_tsv
from cluster.database.db import get_db
from cluster.database.error import abort_400_trace

class Table(object):

    def _transform_data_type(s, oldValue, newValue):

        # Convert the value to the expected data type.
        # We only handle int, float, str.
        dtype = type(oldValue).__name__
        val = None
        print('dtype:', dtype)
        if dtype == 'int' or dtype == 'long':
            val = int(newValue)
        elif dtype == 'float':
            val = float(newValue)
        else:
            val = newValue
        print('_transform_data_type:', type(val).__name__)
        return val

    def _get_one(s, name):
       return get_db().execute(
            'SELECT * FROM ' + s.table + ' WHERE name = ?', (name,)).fetchone()

    def _get_vals(s, data, name=None):

        # Extract the values of a data dict, leaving out foreign key names.
        vals = []
        for key in data.keys():
            if not key in s.foreign_key_names:
                vals.append(data[key])
        return vals

    def _row_header_to_tsv(s, row):
        return s._row_to_tsv(row.keys())

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

    def _update_foreign_key(s,data):

        # Update the foreign key ID given its name.
        fk_field, fk_id = s._get_foreign_key(get_db(), data)
        if fk_field != None:
            if fk_id == None:
                raise Exception('TODO: text: Parent row does not exist.')
            data[fk_field] = fk_id

    def add(s, data):
        try:
            # Add one row.
            exception_if_tsv()
            db = get_db()
            s._update_foreign_key(data)
            cursor = s._add(data, db)
            db.commit()
            return {"id": cursor.lastrowid}

        except sqlite3.IntegrityError as e:
            abort(400, e)
        except Exception as e:
            abort_400_trace(str(e))

    def delete(s, name):
        try:
            row = s.get(name)
            print('delete:row:', row)
            if row == None:
                raise Exception(s.table + ' table name not found: ' + str(name))
            db = get_db()
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()
            return {'id': row['id']}
        except sqlite3.IntegrityError as e:
            abort(400, 'This row is owned by another row connected by a foreign key. ' + str(e))
        except Exception as e:
            abort_400_trace(str(e))

    def get(s, name=None):
        try:
            # Return one by name or return all rows.
            if name:

                # Return one row by ID.
                exception_if_tsv()
                row = s._get_one(name)
                if row is None:
                    raise (s.table + ' table name not found: ' + str(name))
                return row

            # Return all as TSV.
            elif is_tsv():
                return s._rows_to_tsv(s.get_all_rows())

            # Return all rows as a list of dicts.
            return s._rows_to_list_of_dicts(s.get_all_rows())

        except Exception as e:
            abort_400_trace(str(e))

    def load_tsv(s, parent_name, file_path):
        try:
            db = get_db()
            with open(os.path(current_app.UPLOADS, file_path), 'r') as f:
                f = csv.reader(f, delimiter='\t')
                if not f.fieldnames == s._getFieldnames():
                    raise Exception('field name mismatch')
                for row in f:
                    s._add(row.append(parent_name), db)
            db.commit()
            return {'row_count': f.line_num}

        except sqlite3.IntegrityError as e:
            abort(400, 'TODO: wording: This row has no parent foreign key. ' + str(e))
        except:
            abort_400_trace(str(e))

    def update(s, name, field, value):
        try:
            exception_if_tsv()
            row = dict(s.get(name))
            if row == None:
                raise Exception(s.table + ' table name not found: ' + str(name))

            row[field] = s._transform_data_type(row[field], value)
            db = get_db()
            db.execute(
                 'UPDATE ' + s.table + ' SET ' +
                    field + ' = ?'
                 ' WHERE name = ?',
                 (value, name))
            db.commit()
            return {'id': row['id']}

        except Exception as e:
            abort_400_trace(str(e))
