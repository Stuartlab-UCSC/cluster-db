
# The base class for single table access.

# Gets return data in JSON format or TSV format.
# All other access methods return nothing.
import os, sqlite3
from flask import request
from cluster.database.db import get_db, merge_dicts
import cluster.database.tsv as tsv
import cluster.database.error as err
from cluster.database.error import Bad_tsv_header, Not_found, \
    Parent_not_found, Parent_not_supplied


class Table(object):

    parent = None  # Default to no parent tables.
    child_tables = []  # Default to no child tables

    def _add_one(s, data, db):
        cursor = db.execute(s.add_one_string, list(data.values()))
        return cursor

    def _delete_children(s, row, db):
        # Delete immediate children of a row. If there are any grandchildren,
        # those will need to be deleted first.
        print('children:', s.child_tables)
        for child in s.child_tables:
            db.execute('DELETE FROM ' + child + \
                ' WHERE ' + s.table + '_id = ?', \
                (row['id'],))

    def _get_one(s, name, with_row_id=False):
        if with_row_id:
            fields = '*' # get all fields
        else:
            fields = ','.join(s.fields)  # get all fields sans the row id
        row = get_db().execute( \
            'SELECT ' + fields + ' FROM ' + s.table + ' WHERE name = ?', \
                (name,)).fetchone()
        if row == None:
            raise Not_found(s.table + ': ' + name)
        return row

    def _get_one_with_id(s, name):
        return s._get_one(name, True)

    def _get_parent_by_id(s, parent, id):
        table_name = parent['field']
        cursor = get_db().execute( 'SELECT * FROM ' + table_name + \
            ' WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row == None:
            raise Parent_not_found(table_name + ': ID: ' + id)
        return row

    def _get_parent_by_name(s, parent, name):
        table_name = parent['field']
        cursor = get_db().execute( 'SELECT * FROM ' + table_name + \
            ' WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row == None:
            raise Parent_not_found(table_name + ': ' + name)
        return row

    def _get_parent_id(s, parent, name):
        # Find the parent ID from the given parent name.
        row = s._get_parent_by_name(parent, name)
        return row['id']

    def _get_parent_name(s, parent, id):
        # Find the parent name from the given parent ID.
        row = s._get_parent_by_id(parent, id)
        return row['name']

    def _replace_parent_id_with_name_one_row(s, parent, data, db):
        # Find the parent row.
        field = parent['field']
        parent_name = s._get_parent_name(parent, data[field + '_id'])

        # Add the parent name to the data and remove the parent ID.
        new_data = merge_dicts(data, {})
        new_data[field] = parent_name
        del new_data[field + '_id']
        return new_data

    def _replace_parent_id_with_name_in_rows(s, parent, rows, db):
        new_rows = []
        for row in rows:
             new_rows.append(
                s._replace_parent_id_with_name_one_row(s.parent, row, db))
        return new_rows


    def _replace_parent_name_with_id(s, parent, data, db):
        # Find the parent row.
        field = parent['field']
        parent_id = s._get_parent_id(parent, data[field])

        # Add the parent ID to the data and remove the parent name.
        new_data = merge_dicts(data, {})
        new_data[field + '_id'] = parent_id
        del new_data[field]
        return new_data

    def _transform_data_type(s, oldValue, newValue):
        # Convert the new value to the expected data type.
        # We only handle int, float, str.
        dtype = type(oldValue).__name__
        val = None
        if dtype == 'int' or dtype == 'long':
            val = int(newValue)
        elif dtype == 'float':
            val = float(newValue)
        else:
            val = newValue
        return val

############################################################

    def add_many_tsv(s, tsv_file, parent_name=None):
        try:
            tsv.add_many(s, tsv_file, parent_name)
        except Bad_tsv_header as e:
            return err.abort_bad_tsv_header(e)
        except Parent_not_found as e:
            return err.abort_parent_not_found(e)
        except Parent_not_supplied as e:
            return err.abort_parent_not_supplied(e)
        except sqlite3.IntegrityError as e:
           return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)

    def add_one(s, data):
        try:
            # Add one row.
            db = get_db()
            if s.parent:
                new_data = s._replace_parent_name_with_id(s.parent, data, db)
                s._add_one(new_data, db)
            else:
                s._add_one(data, db)
            db.commit()

        except Parent_not_found as e:
            return err.abort_parent_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)

    def delete(s, name):
        try:
            db = get_db()
            row = s._get_one(name) # just to throw an error if it doesn't exist
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_has_children()

    def delete_including_children(s, name):
        try:
            row = s._get_one_with_id(name)
            db = get_db()
            s._delete_children(row, db)
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
           return err.abort_has_children()

    def get_all(s, accept):
        # Return all rows.
        fields = ','.join(s.fields)
        db = get_db()
        cursor = db.execute('SELECT ' + ','.join(s.fields) + ' FROM ' + s.table)
        rows = cursor.fetchall()
        if s.parent:
             rows = s._replace_parent_id_with_name_in_rows(s.parent, rows, db)
        if tsv.requested(accept):
            return tsv.from_rows(s.tsv_header, rows)
        return rows

    def get_by_parent(s, parent_name, accept):
        # Return rows with the given parent, without the parent column.
        try:
            parent_id = s._get_parent_id(s.parent, parent_name)
            id_field = s.parent['field'] + '_id'
            cursor = get_db().execute('SELECT ' + ','.join(s.parentless_fields) + \
                                ' FROM ' + s.table + \
                                ' WHERE ' + id_field + \
                                ' = ' + str(parent_id))
            rows = cursor.fetchall()
            if len(rows) < 1:
                raise Not_found(
                    'with ' + s.parent['field'] + ': ' + parent_name)
            if tsv.requested(accept):
                return tsv.from_rows(s.parentless_fields, rows)
            return rows

        except Not_found as e:
            return err.abort_not_found(e)
        except Parent_not_found as e:
            return err.abort_parent_not_found(e)

    def get_one(s, name, accept):
        try:
            row = s._get_one(name)
            if s.parent:
                row = s._replace_parent_id_with_name_one_row(
                    s.parent, row, get_db())
            if tsv.requested(accept):
                return tsv.from_rows(s.tsv_header, [row])
            return row

        except Not_found as e:
            return err.abort_not_found(e)

    def update(s, name, field, value):
        try:
            row = s._get_one(name) # so we can find the value type
            row[field] = s._transform_data_type(row[field], value)
            db = get_db()
            db.execute(
                 'UPDATE ' + s.table + ' SET ' +
                    field + ' = ?'
                 ' WHERE name = ?',
                 (value, name))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except KeyError:
            return err.abort_keyError(field)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
