
import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.db import dicts_equal, merge_dicts


def test_add_many_tsv(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset.tsv')
        assert result == None
        result = dataset.get_all(ad.accept_json)
        assert dicts_equal(result[0], ad.add_one_dataset)
        assert dicts_equal(result[1], ad.add_second_dataset)


def test_add_many_tsv_bad_header(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_bad_header.tsv')
        assert result == '400 Bad TSV header:\n' + \
                                    'expected: "name species"\n' + \
                                    '   given: "bad header"'


def test_add_many_tsv_too_many_columns(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_too_many_columns.tsv')
        assert result == '400 Database: Wrong number of columns ' + \
            'supplied for add: Incorrect number of bindings supplied. The ' + \
            'current statement uses 2, and there are 3 supplied.'


def test_add_many_tsv_not_enough_columns(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_not_enough_columns.tsv')
        assert result == \
            '400 Database: NOT NULL constraint failed: dataset.species'


def test_add_one(app, client):
    with app.app_context():
        result = dataset.add_one(ad.add_one_dataset)
        assert result == None
        result = dataset.get_one('dataset1', ad.accept_json)
        assert dicts_equal(result, ad.add_one_dataset)


def test_add_one_get_all_get_one_json_api(client):
    # add one
    response = client.post('/api/dataset/add',
        data=json.dumps(ad.add_one_dataset), headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    # get all
    response = client.get('/api/dataset', headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], ad.add_one_dataset)
    # get one
    response = client.get('/api/dataset/dataset1', headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json, ad.add_one_dataset)
    # update
    response = client.get(
        '/api/dataset/update/name/dataset1/field/name/value/dataset3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/dataset', headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], ad.add_third_dataset)
    # delete
    response = client.get('/api/dataset/delete/dataset3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/dataset/dataset3')
    assert response.json == '404 Not found: dataset: dataset3'


def test_tsv_api(client):
    # add one
    response = client.get('/api/dataset/add_many/tsv_file/dataset.tsv')
    assert response.content_type == ad.accept_json
    # get all
    response = client.get('/api/dataset', headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data == b'name\tspecies\ndataset1\tdog\ndataset2\tcat'
    # get one
    response = client.get('/api/dataset/dataset1', headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data == b'name\tspecies\ndataset1\tdog'
    # update
    response = client.get(
        '/api/dataset/update/name/dataset1/field/name/value/dataset3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/dataset', headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data == b'name\tspecies\ndataset3\tdog\ndataset2\tcat'
    # delete
    response = client.get('/api/dataset/delete/dataset3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/dataset/dataset3', headers=ad.tsv_headers)
    assert response.data == b'404 Not found: dataset: dataset3'



def test_add_duplicate(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.add_one(ad.add_one_dataset)
        assert result == \
            '400 Database: UNIQUE constraint failed: dataset.name'


def test_get_all_of_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_all(ad.accept_json)
        assert len(result) == 1
        assert dicts_equal(result[0], ad.add_one_dataset)


def test_get_all_of_one_as_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_all(ad.accept_tsv)
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_all_of_two(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        dataset.add_one(ad.add_second_dataset)
        result = dataset.get_all(ad.accept_json)
        assert len(result) == 2
        assert dicts_equal(result[0], ad.add_one_dataset)
        assert dicts_equal(result[1], ad.add_second_dataset)


def test_get_all_of_two_as_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        dataset.add_one(ad.add_second_dataset)
        result = dataset.get_all(ad.accept_tsv)
        assert len(result) == 38
        assert result == 'name\tspecies\ndataset1\tdog\ndataset2\tcat'
        # TODO test all fields after dataset fields are firmed up.


def test_get_all_with_none(app):
    with app.app_context():
        result = dataset.get_all(ad.accept_json)
        assert len(result) == 0


def test_get_by_parent(app):
    # Datasets have no parent.
    pass


def test_get_by_parent_child_not_found(app):
    # With no parent table, this will never happen.
    pass


def test_get_by_parent_parent_not_found(app):
    # With no parent table, this will never happen.
    pass


def test_get_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_one('dataset1', ad.accept_json)
        assert result['name'] == 'dataset1'


def test_get_one_as_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.get_one('dataset1', ad.accept_tsv)
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_one_not_found(app):
    with app.app_context():
        result = dataset.get_one('dataset1', ad.accept_json)
        print('result:', result)
        assert result == '404 Not found: dataset: dataset1'


def test_update(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.update('dataset1', 'species', 'newt')
        assert result == None
        result = dataset.get_one('dataset1', ad.accept_json)
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
# danger
def test_delete_including_children_no_children(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.delete_including_children('dataset1')
        assert result == None
        result = dataset.get_one('dataset1', ad.accept_json)
        assert result['message'] == '404 Not found: dataset: dataset1'


def test_delete_including_children_with_children(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        clustering_solution.add_one(ad.add_second_clustering_solution)
        result = dataset.delete_including_children('dataset1')
        assert result == None
        result = dataset.get_one('dataset1', ad.accept_json)
        assert result['message'] == '404 Not found: dataset: dataset1'
        result = clustering_solution.get_all(ad.accept_json)
        assert len(result) == 0


def test_delete_including_children_this_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = dataset.delete_including_children('dataset666')
        assert result['message'] == '404 Not found: dataset: dataset666'
"""

