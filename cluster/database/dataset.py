
from flask_user import current_user
from cluster.database import db
from cluster.database.models import Dataset

def all_datasets():
    """
    Return all data sets from the data set table.
    :return: a list of dictionaries {name: (string), description: (string), id: (int) }
    """
    #print('all_datasets: current_user:', current_user)
    return db.session.query(Dataset).all()
