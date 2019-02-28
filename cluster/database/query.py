
# A generic read-only SQL query.

import sqlite3
from flask import request
from cluster.database.db import get_db
import cluster.database.error as err
from cluster.database.error import Not_found, Updates_not_allowed
import cluster.database.tsv as tsv

from cluster.database_update.cluster_attribute_table import cluster_attribute
from cluster.database_update.cell_of_cluster_table import cell_of_cluster
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.dataset_table import dataset
from cluster.database_update.gene_set_table import gene_set
from cluster.database_update.gene_of_set_table import gene_of_set

def query(query):
    try:
        # Don't allow updates to the database, only reads.
        lq = query.lower()
        if 'alter' in lq \
            or 'commit' in lq \
            or 'create' in lq \
            or 'delete' in lq \
            or 'drop' in lq \
            or 'insert' in lq \
            or 'reindex' in lq \
            or 'repace' in lq \
            or 'rollback' in lq \
            or 'update' in lq \
            or 'upsert' in lq \
            :
            raise Updates_not_allowed
        cursor = get_db().execute(query)
        return tsv.from_rows(cursor.fetchall())
    except Updates_not_allowed as e:
        return err.updates_not_allowed(e)
    except Not_found as e:
        return err.abort_not_found(e)
    except sqlite3.IntegrityError as e:
        return err.abort_database(e)
    except sqlite3.ProgrammingError as e:
        return err.abort_database(e)
    except sqlite3.OperationalError as e:
        return err.abort_database(e)

