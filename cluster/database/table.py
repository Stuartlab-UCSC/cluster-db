
# The base class for single table access.

# Gets return data in JSON format or TSV format.
# All other access methods return nothing.
import os, sqlite3
from flask import request
from cluster.database.db import get_db
import cluster.database.tsv as tsv
import cluster.database.error as err
from cluster.database.error \
    import Bad_tsv_header, Not_found, No_parent_table, No_parent_row


class Table(object):

    # Default is no parent table.
    parent_info = None # Default to no parent tables.
    parent_tables = []  # Default to no parent tables.
    # TODO do we need both of the above?

    def _add_one(s, data, db):
        cursor = db.execute(s.add_one_string, s._get_vals(data))
        return cursor

    def _get_parent_info_by_name(s, parent_name):
        # TODO this only handles those tables with only one parent table.
        # Override this for any tables with more than one parent? or some
        # other solution.

        # Find the parent info.
        parent = s.parent_info
        if parent == None:
            raise No_parent_table(s.table)

        # Find the parent row.
        parent_row = parent_table._get_one(parent['id'])
        if parent_row == None:
            raise No_parent_row(parent['table'] + ': ' + parent_name)

        # Return the parent nfo.
        return parent

    def _get_one(s, name, with_id=False):
        if with_id:
            fields = '*'
        else:
            fields = ','.join(s.fields)
        row = get_db().execute( \
            'SELECT ' + fields + ' FROM ' + s.table + ' WHERE name = ?', \
                (name,)).fetchone()
        if row == None:
            raise Not_found(s.table + ': ' + name)
        return row

    def _get_one_with_id(s, name):
        return s._get_one(name, True)

    def _get_vals(s, data):
        vals = []
        for field in s.fields:
            vals.append(data[field])
        return vals

    def _replace_parent_name_with_id(s, data, db):
        # TODO only works with one parent.
        parent = s.parent_info

        # Find the parent row.
        parent_row = parent_table._get_one(parent['id'])
        if parent_row == None:
            raise Exception('Parent row does not exist with the name: ' +
                            data[parent['id']])

        # Add the parent ID to the data and remove the parent name.
        data[parent['id_field']] = parent_row['id']
        del data[parent['name_field']]

    def _transform_data_type(s, oldValue, newValue):
        # Convert the value to the expected data type.
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

    def add_many_tsv(s, tsv_file, parent_names=None):
        try:
            tsv.add_many(s, tsv_file, parent_names)
        except Bad_tsv_header as e:
            return err.abort_bad_tsv_header(e)
        except sqlite3.IntegrityError as e:
           return err.abort_no_parent(e)

    def add_one(s, data):
        try:
            # Add one row.
            db = get_db()
            if s.parent_info != None:
                s._replace_parent_name_with_id(s, data, db)
            s._add_one(data, db)
            db.commit()

        except sqlite3.IntegrityError as e:
            return err.abort_database(e)

    def delete(s, name):
        try:
            db = get_db()
            row = s._get_one(name)
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)

    def delete_with_children(s, name):
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
        db = get_db()
        fields = ','.join(s.fields)
        print('fields:', fields)
        cursor = db.execute('SELECT ' + ','.join(s.fields) + ' FROM ' + s.table)
        rows = cursor.fetchall()
        print('rows:', rows)
        if tsv.requested(accept):
            return tsv.from_rows(rows, s.fields)
        return rows

    def get_by_parent(s, parent_name, accept):

        # Return rows with the given parent, removing the parent and ID fields.
        try:
            parent = s._get_parent_info_by_name(parent_name)
            db = get_db()
            cursor = db.execute('SELECT ' + ' '.join(s.fields) +
                                ' FROM ' + s.table +
                                ' WHERE ' + parent['id_field'] +
                                ' = ' + str(parent['_id']))
            rows = cursor.fetchall()
            if tsv.requested(accept):
                return tsv.from_rows(rows)
            return rows

        except No_parent_row as e:
            return err.abort_no_parent_row(e)
        except No_parent_table as e:
            return err.abort_no_parent_table(e)

    def get_one(s, name, accept):
        try:
            row = s._get_one(name)
            if tsv.requested(accept):
                return tsv.from_rows([row], s.fields)
            return row

        except Not_found as e:
            return err.abort_not_found(e)

    def update(s, name, field, value):
        try:
            row = s._get_one(name)

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

