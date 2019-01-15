
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.attribute_table import attribute
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_attribute, {})
del(one_data_got_by_parent['cluster'])
one_second_data_got_by_parent = merge_dicts(ad.add_one_second_attribute, {})
del(one_second_data_got_by_parent['cluster'])
second_data_got_by_parent = merge_dicts(ad.add_second_attribute, {})
del(second_data_got_by_parent['cluster'])

# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(
        ad.add_one_clustering_solution, ['dataset1'])
    cluster.add_one(ad.add_one_cluster, ['clustering_solution1', 'dataset1'])
    cluster.add_one(ad.add_second_cluster, ['clustering_solution1', 'dataset1'])


def test_add_tsv_and_get_by_clustering_solution(app):
    with app.app_context():
        add_parents()
        result = attribute.add_tsv(
            'attribute.tsv', ['clustering_solution1', 'dataset1'])
        assert result == None

        #result = attribute.get_all(ad.accept_json)
        #print('result', result)
        #assert False

        result = attribute.get_by_clustering_solution_clusters(
            ['clustering_solution1', 'dataset1'], ad.accept_json)
        assert dicts_equal(result[0], ad.add_one_attribute)
        assert dicts_equal(result[1], ad.add_second_attribute)
        assert dicts_equal(result[2], ad.add_one_second_attribute)
        assert dicts_equal(result[3], ad.add_second_second_attribute)


def test_get_by_clustering_solution_clustering_solution_not_found(app):
    with app.app_context():
        add_parents()
        attribute.add_tsv(
            'attribute.tsv', ['clustering_solution1', 'dataset1'])
        result = attribute.get_by_parent(
            ['clustering_solutionX', 'dataset1'], ad.accept_json)
        assert result == \
            '404 Not found: clustering_solution: clustering_solutionX'


def test_tsv_api(app, client):
    # add many tsv
    add_parents()
    cluster.add_one(ad.add_second_cluster, ['clustering_solution1', 'dataset1'])
    response = client.get(
        '/api/attribute/add' + \
        '/tsv_file/attribute.tsv' + \
        '/clustering_solution/clustering_solution1' + \
        '/dataset/dataset1')
    assert response.content_type == ad.accept_json
    assert response.data.decode("utf-8") == 'null\n'

    # get by parent
    response = client.get(
        '/api/attribute/get_by' + \
        '/clustering_solution/clustering_solution1' + \
        '/dataset/dataset1',
         headers=ad.tsv_headers)
    print('response.json:', response.json)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	value	cluster
attribute1	value11	cluster1
attribute2	value21	cluster1
attribute1	value12	cluster2
attribute2	value22	cluster2'''
"""
    # update
    response = client.get('/api/attribute/update/name' + \
        '/attribute/field/name/value/attribute3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/attribute/attribute3',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	value	cluster
attribute3	value1	cluster1'''

    # delete
    response = client.get(
        '/api/attribute/delete/attribute3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/attribute/attribute3',
        headers=ad.tsv_headers)
    assert response.data.decode("utf-8") == \
        '404 Not found: attribute: attribute3'
"""

def test_json_api(app, client):
    # get by clustering_solution
    add_parents()
    client.get(
        '/api/attribute/add' + \
        '/tsv_file/attribute.tsv' + \
        '/clustering_solution/clustering_solution1' + \
        '/dataset/dataset1')

    #response = client.get('/api/attribute', headers=ad.json_headers)
    #print('response.data', response.data)
    #assert False

    response = client.get(
        '/api/attribute/get_by' + \
        '/clustering_solution/clustering_solution1' + \
        '/dataset/dataset1',
         headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], ad.add_one_attribute)
    assert dicts_equal(response.json[1], ad.add_second_attribute)
    assert dicts_equal(response.json[2], ad.add_one_second_attribute)
    assert dicts_equal(response.json[3], ad.add_second_second_attribute)
"""
    # update
    response = client.get('/api/attribute/update/name/' + \
        'attribute1/field/name/value/attribute3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/attribute/attribute3',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    print('response.json:', response.json)
    assert dicts_equal(response.json, one_data_updated)

    # delete
    response = client.get('/api/attribute/delete/attribute3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/attribute/attribute3')
    assert response.json == '404 Not found: attribute: attribute3'
"""

