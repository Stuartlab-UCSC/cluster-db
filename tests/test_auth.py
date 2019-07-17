
import os, json, csv
import pytest
from flask import current_app, url_for, request
from flask_login import login_user, encode_cookie
from flask_user import current_user

from cluster.database import db
from cluster.database.dataset import all_datasets
from cluster.auth.db_models import User
from cluster.database.models import Dataset

import tests.access_db_data as ad
#from cluster.database.pre_sqlAlchemy import dicts_equal, merge_dicts


# Add datasets from the tsv file.
def add_datasets(session):
    path = os.path.join(current_app.config['UPLOADS'], 'dataset.tsv')
    with open(path, 'rU') as fin:
        fin = csv.DictReader(fin, delimiter='\t')
        for row in fin:
            #print('name:', row['name'])
            oRow = Dataset(
                name=row['name'],
                uuid=row['uuid'],
                species=row['species'],
                organ=row['organ'],
                cell_count=row['cell_count'],
                disease=row['disease'],
                platform=row['platform'],
                description=row['description'],
                data_source_url=row['data_source_url'],
                role=row['role']
            )
            db.session.add(oRow)
            db.session.commit()


def test_get_default_user(app):
    res = User.query.first()
    assert res.id == 1
    assert res.active == True
    assert res.email == 'admin@replace.me'
    assert res.email_confirmed_at
    assert res.roles

# TODO test more on users and roles.


def test_get_all_dataset_by_db(session):
    add_datasets(session)
    res = list(Dataset.query)
    assert len(res) == 3
    for row in res:
        if row.id == 1:
            assert row.name == 'dataset1'
        if row.id == 2:
            assert row.name == 'dataset2'
        if row.id == 3:
            assert row.name == 'dataset3'


def test_get_all_datasets_by_db_access(session):
    user = User.query.first()
    login_user(user)
    assert current_user.email == 'admin@replace.me'
    
    add_datasets(session)

    res = all_datasets()
    assert len(res) == 3
    for row in res:
        if row.id == 1:
            assert row.name == 'dataset1'
        if row.id == 2:
            assert row.name == 'dataset2'
        if row.id == 3:
            assert row.name == 'dataset3'

'''
def test_get_all_datasets_by_api(session, client):
    ...
    res = client.get('/dataset')
    assert res.status_code == 200
    print ('res.json:', res.json)
    
    data = res.json['resource']
    assert data[0]['name'] == 'dataset1'
    assert data[1]['name'] == 'dataset2'
    assert data[2]['name'] == 'dataset3'
    assert False
'''

