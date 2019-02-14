
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
        # Query with joins to find the table row's parent ID.
        # TODO it may be better incorporate this in to each SQL query
        # rather than do this additional query to find the parent ID.
        id = -1
        query = \
            'SELECT ' + s.parent_table[0] + '.id as id' + \
            ' FROM ' + s.parent_table[0]
        join_query = ''
        where_query = ' WHERE '
        length = len(parent_name)

        # Walk the parent table and name lists in reverse
        # to build up the WHERE and JOIN clauses.
        for i in range(length -1, -1, -1):
            table = s.parent_table[i]
            name = parent_name[i]
            
            # append to the JOIN part of query.
            if length > 1 and i > 0:
                join_query += ' INNER JOIN ' + table + ' ON ' + table + '.id = ' + \
                    s.parent_table[i-1] + '.' + table + '_id'
            
            # append to the WHERE part of query
            if i < (length - 1):
                where_query += ' and '
            where_query += table + '.name = "' + name + '"'
            
        query += join_query + where_query
        row = get_db().execute(query).fetchone()
        if row == None:
            raise Not_found('parent')
        id = row['id']
        return id

    def _get_closest_parent_id_by_name_in_child_row(s, row, parent_name):
        # The parent_name here lacks the closest parent which is in the row,
        # so add that parent name to the given parent names.
        
        # TODO It may be better to include the parent name in the endpoint's URL
        # rather than in the post payload. Then this function would not be
        # needed. It is only used when adding a clustering_solution or signature
        # _gene_set.
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
        # This should only be used by tables where the usual method is to add
        # one row at a time. Other tables should use add_tsv.
        # (for dataset, clustering_solution, signature_gene_set)
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
        # This should only be used by tables where the usual method is to add
        # multiple rows via a tsv file. Other tables should use add_one.
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

    def delete_by_parent(s, parent_name):
    	# Delete all of the children in this table by the parent.
        try:
            db = get_db()
            parent_id = s._get_closest_parent_id_by_name(parent_name)
            db.execute('DELETE FROM ' + s.table + \
                ' WHERE '  + s.parent_table[0] + '_id = ' + str(parent_id))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_has_children()

    def delete_by_clustering_solution_clusters(s, parent_name):
    	# Delete all of the children of all clusters in a clustering_solution.
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
                    'DELETE FROM ' + s.table + \
                    ' WHERE cluster_id = ' + str(cluster_id)
                cursor = db.execute(query)
            return ''

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_has_children()

    def delete_one(s, name, parent_name=None):
        # Parents is an array of parent names, closest to farthest.
        try:
            db = get_db()
            if parent_name:
                parent_id = s._get_closest_parent_id_by_name(parent_name)
                row = s._get_one(name) # throw an error if not found
                db.execute('DELETE FROM ' + s.table + \
                    ' WHERE name = ? AND '  + s.parent_table[0] + '_id = ?',
                    (name, parent_id))
            else:
                row = s._get_one(name) # throws an error if not found
                db.execute('DELETE FROM ' + s.table + ' WHERE name = ?', (name,))
            db.commit()

        except Not_found as e:
            return err.abort_not_found(e)
        except sqlite3.IntegrityError as e:
            return err.abort_has_children()

    def get_all(s):
        # Return all rows. Parents are returned as IDs rather than names.
        fields = ','.join(s.fields)
        db = get_db()
        query = 'SELECT ' + ','.join(s.fields) + ' FROM ' + s.table
        cursor = db.execute(query)
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

