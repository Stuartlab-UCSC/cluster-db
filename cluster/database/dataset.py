
from cluster.database.models import Dataset

def all_datasets():
    """
    Return all data sets from the data set table.
    :return: a list of dictionaries {name: (string), description: (string), id: (int) }
    """
    return Dataset.query(name, desription, id)

