
# The base class for single table access.

# Gets return data in JSON format or TSV format.
# All other access methods return nothing.
import os, sqlite3
from flask import request
from cluster.database.db import get_db, merge_dicts
import cluster.database.error as err
from cluster.database.error import Bad_tsv_header, Not_found
import cluster.database.tsv as tsv
import cluster.database.util as util

class Table(object):

    def _add_one(s, row, db):
        query = \
            'INSERT INTO ' + s.table + ' (' + \
                ','.join(s.fields) + \
            ') ' + \
            'VALUES (' + ('?,' * len(s.fields))[:-1] + ')'
        cursor = db.execute(query, list(row.values()))
        return cursor.lastrowid

    """ unused for now.
    def _delete_children(s, row, db):
        # Delete immediate children of a row. If there are any grandchildren,
        # those will need to be deleted first.
        for child in s.child_table:
            db.execute('DELETE FROM ' + child + \
                ' WHERE ' + s.table + '_id = ?', \
                (row['id'],))
    """

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

    def _get_closest_parent_id_by_name(s, parent_name):
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
                raise Not_found(table + ': ' + name)
            id = row['id']
        return id

    def _get_closest_parent_id_by_name_in_child_row(s, row, parent_name):
        # The parent_name here lacks the closest parent which is in the row,
        # so add that parent name to the given parent names.
        parent_names = [row[s.parent_table[0]]]
        if parent_name:
            parent_names += parent_name
        return s._get_closest_parent_id_by_name(parent_names)

    def _get_parent_name(s, parent_table, parent_id):
        # Find the parent name from the given parent table name and parent ID.
        row = get_db().execute(
            'SELECT * FROM ' + parent_table + \
            ' WHERE id = "' + str(parent_id) + '"' \
            ).fetchone()
        if row == None:
            raise Not_found(parent_table + ': ID: ' + parent_id)
        return row['name']

    def _replace_unique_parent_id_with_name_in_rows(
        s, parent_table, parent_id, rows, db):
        # Replace the parent ID with its name in all rows
        # where the parent is the same.
        if len(rows) < 1:
            return []
        parent_name = s._get_parent_name(
            parent_table, rows[0][parent_table + '_id'])
        new_rows = []
        for row in rows:
            new_row = merge_dicts(row, {})
            new_row[parent_table] = parent_name
            del new_row[parent_table + '_id']
            new_rows.append(new_row)
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
                parent_id = s._get_closest_parent_id_by_name_in_child_row(
                    row, parent_name)
                parent_table = s.parent_table[0]
                new_row = merge_dicts(row, {})
                new_row[parent_table + '_id'] = parent_id
                # Remove the parent name.
                del new_row[parent_table]
                rowId =s._add_one(new_row, db)
            else:
                rowId = s._add_one(row, db)
            db.commit()
            return rowId

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)

    def add_tsv(s, tsv_file, parent_name=None):
        try:
            return tsv.add(s, tsv_file, parent_name)
        except Bad_tsv_header as e:
            return err.abort_bad_tsv_header(e)
        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_database(e)
        except sqlite3.ProgrammingError as e:
            return err.abort_database(e)
        except FileNotFoundError as e:
            return err.abort_not_found('file: ' + tsv_file)
    """
    def delete(s, name, parent_name=None):
        # Parents is an array of parent names, closest to farthest.
        try:
            db = get_db()
            if parent_name:
                parent_id = s._get_closest_parent_id_by_name(parent_name)
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
            row = s._get_one(name, True)
            db = get_db()
            s._delete_children(row, db)
            db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
           return err.abort_has_children()
    """
    def get_all(s):
        # Return all rows. Parents are returned as IDs rather than names.
        fields = ','.join(s.fields)
        db = get_db()
        cursor = db.execute('SELECT ' + ','.join(s.fields) + ' FROM ' + s.table)
        return(tsv.from_rows(cursor.fetchall()))

    def get_by_clustering_solution_clusters(s, parent_name):
        # Special for retrieving by all clusters in a clustering solution.
        try:
            # Find all of the clusters for the given clustering_solution.
            cluster_rows = util.get_by_parent(s.cluster_table,
                parent_name, return_ids=True)
            # Find child rows for each cluster querying once per cluster.
            db = get_db()
            rows_of_rows = []
            for cluster_row in cluster_rows:
                cluster_id = cluster_row['id']
                query = \
                    'SELECT ' + ','.join(s.fields) + \
                    ' FROM ' + s.table + \
                    ' WHERE cluster_id = ' + str(cluster_id)
                cursor = db.execute(query)
                rows = cursor.fetchall()
                # Trade the cluster ID for the cluster name in the rows.
                rows_of_rows += s._replace_unique_parent_id_with_name_in_rows(
                    'cluster', cluster_id, rows, db)

            if len(rows_of_rows) < 1:
                raise Not_found(s.table + ' with ' + s.parent_table[0] + \
                    ': ' + parent_name[0] + ' or with cluster names')
            return tsv.from_rows(rows_of_rows)

        except Not_found as e:
            return err.abort_not_found(e)

    def get_by_parent(s, parent_name):
        # Return rows with the given parent names, without the parent column.
        # Parents is an array of parent names, closest to farthest.
        try:
            return tsv.from_rows(util.get_by_parent(s, parent_name))
        except Not_found as e:
            return err.abort_not_found(e)


    def get_one(s, name):
        # Only works for tables with no parent tables.
        try:
            row = s._get_one(name)
            return tsv.from_rows([row])

        except Not_found as e:
            return err.abort_not_found(e)
    """
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
    """