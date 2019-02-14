
import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.db import dicts_equal, merge_dicts

one_data_field_missing = merge_dicts(ad.add_one_dataset, {})
del one_data_field_missing['species']


def test_add_two_and_get_all_delete(app):
    with app.app_context():
        result = dataset.add_one(ad.add_one_dataset)
        assert result == 1
        result = dataset.add_one(ad.add_second_dataset)
        assert result == 2
        
        # verify adds
        result = dataset.get_all()
        print('result:', result)
        assert result == \
'''name	species
dataset1	dog
dataset2	cat'''

        # delete one
        result = dataset.delete_one('dataset1')
        assert result == None
        
        # verify delete
        result = dataset.get_all()
        print('result:', result)
        assert result == \
'''name	species
dataset2	cat'''


def test_add_one_field_missing(app):
    with app.app_context():
        result = dataset.add_one(one_data_field_missing)
        assert result == '400 Database: Wrong number of columns supplied ' + \
            'for add: Incorrect number of bindings supplied. The current ' + \
            'statement uses 2, and there are 1 supplied.'


def test_add_one_duplicate(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.add_one(ad.add_one_dataset)
        assert result == '400 Database: UNIQUE constraint failed: dataset.name'


def test_add_tsv(app):
    with app.app_context():
        result = dataset.add_tsv('dataset.tsv')
        assert result == 2
        result = dataset.get_all()
        assert result == \
'''name	species
dataset1	dog
dataset2	cat'''


def test_add_tsv_bad_header(app):
    with app.app_context():
        result = dataset.add_tsv('dataset_bad_header.tsv')
        assert result == '400 Bad TSV header:\n' + \
                                    'expected: "name species"\n' + \
                                    '   given: "bad header"'


def test_add_tsv_too_many_columns(app):
    with app.app_context():
        result = dataset.add_tsv('dataset_too_many_columns.tsv')
        assert result == '400 Database: Wrong number of columns ' + \
            'supplied for add: Incorrect number of bindings supplied. The ' + \
            'current statement uses 2, and there are 3 supplied.'


def test_add_tsv_not_enough_columns(app):
    with app.app_context():
        result = dataset.add_tsv('dataset_not_enough_columns.tsv')
        assert result == \
            '400 Database: NOT NULL constraint failed: dataset.species'


def test_add_tsv_duplicate(app):
    with app.app_context():
        result = dataset.add_tsv('dataset_duplicate.tsv')
        assert result == '400 Database: UNIQUE constraint failed: dataset.name'


def test_delete(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.delete_one('dataset1')
        assert result == None
        result = dataset.get_one('dataset1')
        assert result == '404 Not found: dataset: dataset1'


def test_delete_not_found(app):
    with app.app_context():
        result = dataset.delete_one('dataset1')
        assert result == '404 Not found: dataset: dataset1'


def test_delete_has_children(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        cluster_solution.add_one(ad.add_one_cluster_solution)
        result = dataset.delete_one('dataset1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_get_all_of_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_all()
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_all_with_none(app):
    with app.app_context():
        result = dataset.get_all()
        assert len(result) == 0


def test_get_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_one('dataset1')
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_one_not_found(app):
    with app.app_context():
        result = dataset.get_one('dataset1')
        assert result == '404 Not found: dataset: dataset1'

"""
def test_update(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.update('dataset1', 'species', 'newt')
        assert result == None
        result = dataset.get_one('dataset1')
        assert result['species'] == 'newt'


def test_update_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.update('dataset666', '_id', 666)
        assert result == '404 Not found: dataset: dataset666'


def test_update_id(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.update('dataset1', '_id', 666)
        assert result == "400 Database: invalid field: _id"


def test_update_bad_field(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.update('dataset1', 'junkField', 666)
        assert result == "400 Database: invalid field: junkField"
"""


def test_add_two_api(client):
    # add two
    response = ad.post_json(client, '/api/dataset/add', ad.add_one_dataset)
    assert response.content_type == ad.text_plain
    #print('response.data:', response.data)
    assert response.data.decode("utf-8") == '1'

    response = ad.post_json(client, '/api/dataset/add', ad.add_second_dataset)
    assert response.content_type == ad.text_plain
    #print('response.data:', response.data)
    assert response.data.decode("utf-8") == '2'

    # get all
    response = client.get('/api/dataset')
    #print('response:',response)
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	species
dataset1	dog
dataset2	cat'''

    # delete one
    response = client.get('/api/dataset/delete/dataset1')
    print('response:',response)
    print('response.decode:',response.data.decode("utf-8"))
    assert response.content_type == ad.text_plain

    # get all
    response = client.get('/api/dataset')
    print('response:',response)
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	species
dataset2	cat'''

    # delete one not there
    response = client.get('/api/dataset/delete/dataset1')
    print('response:',response)
    print('response.decode:',response.data.decode("utf-8"))
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
    	'404 Not found: dataset: dataset1'

def test_api(client):
    # add tsv
    response = client.get('/api/dataset/add/tsv_file/dataset.tsv')
    assert response.content_type == ad.text_plain
    print('response.data', response.data)
    assert response.data.decode("utf-8") == '2'

    # get all
    response = client.get('/api/dataset')
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	species
dataset1	dog
dataset2	cat'''

    # get one
    response = client.get('/api/dataset/dataset1')
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	species
dataset1	dog'''
