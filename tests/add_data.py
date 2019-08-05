
from tests.dataset_entries import entries

def add_entry(session, table, **kwargs):

    entry = table(**kwargs)
    session.add(entry)
    session.commit()


def add_entries(session, entries=entries):
    [add_entry(session, table, **kwargs) for table, kwargs in entries]