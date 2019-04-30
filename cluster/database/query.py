
# A generic read-only SQL query.
import sqlite3
from cluster.database.pre_sqlAlchemy import get_db
import cluster.database.error as err
from cluster.database.error import Not_found, Updates_not_allowed
import cluster.database.tsv as tsv


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

