
from sqlalchemy.exc import IntegrityError


def add_entry(session, table, **kwargs):
    entry = table(**kwargs)
    try:
        session.add(entry)
        session.commit()

    except IntegrityError as e:
        if "UNIQUE constraint failed" in e.args[0]:
            session.rollback()
            pass

def add_entries(session, entries):
    [add_entry(session, table, **kwargs) for table, kwargs in entries]

