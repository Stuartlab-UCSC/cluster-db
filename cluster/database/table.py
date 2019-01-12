
# The base class for single table access.

# Gets return data in JSON format or TSV format.
# All other access methods return nothing.
import os, sqlite3
from flask import request
from cluster.database.db import get_db, merge_dicts
import cluster.database.tsv as tsv
import cluster.database.error as err
from cluster.database.error import Bad_tsv_header, Not_found, \
    Parent_not_found


class Table(object):

    def __init__(s):
        s.parent_table = None  # Default to no parent tables.
        s.child_table = []  # Default to no child tables

    def _add_one(s, row, db):
        query = \
            'INSERT INTO ' + s.table + ' (' + \
                ','.join(s.fields) + \
            ') ' + \
            'VALUES (' + ('?,' * len(s.fields))[:-1] + ')'
        cursor = db.execute(query, list(row.values()))
        return cursor.lastrowid

    def _add_tsv_with_parent(s, parent_name, rows, db):
        parent_id = s._get_closest_parent_id(parent_name)
        query = \
            'INSERT INTO ' + s.table + ' (' + \
                ','.join(s.fields) + \
            ') ' + \
            'VALUES (' + ('?,' * len(s.fields))[:-1] + ')'
        for row in rows:
            row = dict(row)
            row[s.parent_table[0] + '_id'] = parent_id
            query += '(' + row.values() + '),'
        db.execute(query)

    def _delete_children(s, row, db):
        # Delete immediate children of a row. If there are any grandchildren,
        # those will need to be deleted first.
        for child in s.child_table:
            db.execute('DELETE FROM ' + child + \
                ' WHERE ' + s.table + '_id = ?', \
                (row['id'],))

    def _get_one(s, name, with_row_id=False):
        if with_row_id:
            fields = '*' # get all fields
        else:
            fields = ','.join(s.fields)  # get all fields sans the row id
        query = \
            'SELECT ' + fields + \
            ' FROM ' + s.table + \
            ' WHERE name = "' + name + '"'
        row = get_db().execute(query).fetchone()
        if row == None:
            raise Not_found(s.table + ': ' + name)
        return row

    def _get_one_with_id(s, name):
        return s._get_one(name, True)

    def _get_closest_parent_id(s, parent_name):
        id = -1
        # Walk the patent table and name lists in reverse
        # to find the closest parent ID.
        for i in range(len(s.parent_table) -1, -1, -1):
            table = s.parent_table[i]
            name = parent_name[i]
            row = get_db().execute(
                'SELECT * FROM ' + table + \
                ' WHERE name = "' + name + '"' \
                ).fetchone()
            if row == None:
                raise Parent_not_found(table + ': ' + name)
            id = row['id']
        return id

    """
    # TODO should be deprecated, merge with _get_closest_parent_id
    def _get_parent_id(s, parent, name):
        # Find the parent ID from the given parent table name and parent name.
        row = get_db().execute(
            'SELECT * FROM ' + parent + \
            ' WHERE name = "' + name + '"' \
            ).fetchone()
        if row == None:
            raise Parent_not_found(parent + ': ' + name)
        return row['id']
    """

    def _get_parent_name(s, parent, id):
        # Find the parent name from the given parent table name and parent ID.
        row = get_db().execute(
            'SELECT * FROM ' + parent + \
            ' WHERE id = "' + str(id) + '"' \
            ).fetchone()
        if row == None:
            raise Parent_not_found(parent + ': ID: ' + id)
        return row['name']

    def _replace_parent_id_with_name_one_row(s, row, db):
        # Replace the parent ID with its name
        # given the parent table name and a data row.
        parent_table = s.parent_table[0]
        parent_name = s._get_parent_name(row, row[parent_table + '_id'])

        # Add the parent name to the data and remove the parent ID.
        new_row = merge_dicts(row, {})
        new_row[parent_table] = parent_name
        del new_row[parent_table + '_id']
        return new_row

    def _replace_parent_id_with_name_in_rows(s, parent, rows, db):
        # Replace the parent ID with its name
        # given the parent table name and data rows.
        parent_name = s._get_parent_name(parent, data[field + '_id'])
        new_rows = []
        for row in rows:
             new_rows.append(
                s._replace_parent_id_with_name_one_row(parent, row, db))
        return new_rows

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

    def add_one(s, row, parent_name=None):
        try:
            # Add one row.
            db = get_db()
            if s.parent_table:
                # Add the parent ID to the data.
                parent_id = s._get_closest_parent_id(parent_name)
                parent_table = s.parent_table[0]
                new_row = merge_dicts(row, {})
                new_row[parent_table + '_id'] = parent_id
                # Remove the parent name.
                del new_row[parent_table]
                s._add_one(new_row, db)
            else:
                s._add_one(row, db)
            db.commit()

        except Parent_not_found as e:
            return err.abort_parent_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)

    def add_tsv(s, tsv_file, parent_name=None):
        try:
            tsv.add(s, tsv_file, parent_name)
        except Bad_tsv_header as e:
            return err.abort_bad_tsv_header(e)
        except Parent_not_found as e:
            return err.abort_parent_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)

    def delete(s, name, parent_name=None):
        # Parents is an array of parent names, closest to farthest.
        try:
            db = get_db()
            if parent_name:
                parent_id = s._get_closest_parent_id(parent_name)
                row = s._get_one(name) # throw an error if not found
                db.execute('DELETE FROM ' + s.table + \
                    ' WHERE name = ? AND '  + s.parent + '_id = ?',
                    (name, parent_id))
            else:
                row = s._get_one(name) # throw an error if not found
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
        if s.parent_table:
            rows = s._replace_parent_id_with_name_in_rows(s.parent, rows, db)
            if tsv.requested(accept):
                rows = tsv.from_rows(
                    s.parentless_fields + [s.parent_table[0]], rows)
        else:
            if tsv.requested(accept):
                rows = tsv.from_rows(s.parentless_fields, rows)
        return rows

    def get_by_parent(s, parent_name, accept):
        # Return rows with the given parent names, without the parent column.
        # Parents is an array of parent names, closest to farthest.
        try:
            parent_id = str(s._get_closest_parent_id(parent_name))
            print('parent_id:', parent_id)
            query = \
                'SELECT ' + ','.join(s.parentless_fields) + \
                ' FROM ' + s.table + \
                ' WHERE ' + s.parent_table[0] + '_id' + \
                ' = ' + str(s._get_closest_parent_id(parent_name))
            cursor = get_db().execute(query)
            rows = cursor.fetchall()
            if len(rows) < 1:
                raise Not_found(s.table + ' with ' + s.parent_table[0] + \
                    ': ' + parent_name[0])
            if tsv.requested(accept):
                return tsv.from_rows(s.parentless_fields, rows)
            return rows

        except Not_found as e:
            return err.abort_not_found(e)
        except Parent_not_found as e:
            return err.abort_parent_not_found(e)

    def get_one(s, name, accept):
        # Only works for tables with no parent tables.
        try:
            row = s._get_one(name)
            if tsv.requested(accept):
                return tsv.from_rows(s.parentless_fields, [row])
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
