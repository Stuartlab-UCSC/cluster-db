
# TSV database utilites.
import os, csv, sqlite3
from flask import current_app
from cluster.database.db import get_db, lists_equal, merge_dicts
from cluster.database.error import Bad_tsv_header, Not_found
import cluster.database.util as util


def _add_with_parent_id(table, parent_name, rows, db):
    # Make the first part of the query string without the values.
    query = \
        'INSERT INTO ' + table.table + ' (' + \
            ','.join(table.fields) + \
        ') ' + \
        'VALUES '
    # Find the query values replacing the parent name with parent ID.
    if table.table == 'cluster_attribute':
        query_vals = _values_cluster_attribute(table, parent_name, rows, db)
    elif table.table == 'cell_of_cluster':
        query_vals = _values_cell_of_cluster(table, parent_name, rows, db)
    else:
        query_vals = _values_same_parent(table, parent_name, rows, db)
    # Execute the query.
    query = query + query_vals[:-1]
    cursor = db.execute(query) # remove trailing comma
    return cursor.lastrowid


def _get_clusters(table, parent_name):
    # Return a dict of cluster names to cluster IDs.
    cluster_rows = util.get_by_parent(table.cluster_table,
        parent_name, return_ids=True)
    clusters = {}
    for row in cluster_rows:
        clusters[row['name']] = row['id']
    return clusters


def _get_tsv_fields(table):
    try:
        fields = table.tsv_fields
    except:
        fields = table.parentless_fields
    return fields


def _header_check_cluster_attribute(f_fieldnames, table):
    # Attribute header is only checked for 'cluster'
    # because the rest of the header contains variable names.
    if (f_fieldnames[0] != 'cluster'):
        raise Bad_tsv_header( \
            'expected in first column: "cluster' + \
         '"\n                   given: "' + f_fieldnames[0] + '"')


def _header_check(f_fieldnames, table):
    # Bail if the file header is not correct.
    if (table.table == 'cluster_attribute'):
        _header_check_cluster_attribute(f_fieldnames, table)
    else:
        header = _get_tsv_fields(table)
        if not lists_equal(f_fieldnames, header):
            raise Bad_tsv_header( \
                'expected: "' + ' '.join(header) + \
             '"\n   given: "' + ' '.join(f_fieldnames) + '"')


def _values_cluster_attribute(table, parent_name, rows, db):
    # Special handling due to cluster_attribute TSV file being a matrix of cluster_attribute
    # names by cluster names, with cluster_attribute names as the first row.
    clusters = _get_clusters(table, parent_name)
    query_vals = ''
    for row in rows:
        # Look at a row which contains one cluster's values.
        cluster_id = str(clusters[row['cluster']])
        for attr_name in rows.fieldnames[1:]: # leave out the cluster name
            # Build the values string for each cluster,
            # replacing the cluster name with cluster ID.
            query_vals += '("' + \
                attr_name + '","' + \
                row[attr_name] + '","' + \
                cluster_id + '"),'

    return query_vals


def _values_cell_of_cluster(table, parent_name, rows, db):
    # Special handling due to cell_of_clusters TSV file where each row may
    # have a different parent cluster.
    clusters = _get_clusters(table, parent_name)
    query_vals = ''
    for row in rows:
        # Build the values string for each row,
        # replacing the cluster name with cluster ID.
        val_string = '('
        for val in list(row.values())[:-1]:
            if val == None:
                val_string += 'null,'
            else:
                val_string += '"' + val + '",'
        try:
            cluster_id = str(clusters[row['cluster']])
        except KeyError:
            raise Not_found('cluster name of: ' + str(row['cluster']))
        query_vals += val_string + '"' + cluster_id + '"),'

    return query_vals


def _values_same_parent(table, parent_name, rows, db):
    # Build the values string where all rows have the same parent,
    # replacing the parent name with the parent ID.
    parent_id = table._get_closest_parent_id_by_name(parent_name)
    query_vals = ''
    for row in rows:
        val_string = '('
        for val in list(row.values()):
            if val == None:
                val_string += 'null,'
            else:
                val_string += '"' + val + '",'
        query_vals += val_string + '"' + str(parent_id) + '"),'
    return query_vals


def add(table, tsv_file, parent_name=None):
    # Note: Rows that are too short don't error out,
    #       but will simply add null values at the end.
    #       Rows that are too long are interpreted as a new row and may error
    #       out if non-nulls are required for this bad row.
    f = os.path.join(current_app.config['UPLOADS'], tsv_file)
    with open(f, 'r') as f:
        f = csv.DictReader(f, delimiter='\t')

        # Bail if the file header is not correct.
        _header_check(f.fieldnames, table)
        db = get_db()
        if table.parent_table:
            # Table has parents, so add with the parent ID.
            rowId = _add_with_parent_id(table, parent_name, f, db)
        else:
            # No parents, so simply add to the database.
            for row in f:
                rowId = table._add_one(row, db)

        db.commit()
        return rowId


def from_rows(rows):
    # Convert sqlite rows to TSV lines.
    if len(rows) < 1:
        return ''
    tsv = '\t'.join(rows[0].keys()) # the header
    for row in rows:
        lines = []
        for l in list(row.values()):
            lines.append(str(l))
        tsv += '\n' + '\t'.join(lines)
    return tsv


def requested(accept):
    return (str(accept) == 'text/tab-separated-values')


