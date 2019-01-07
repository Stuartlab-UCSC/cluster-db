
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.cluster_assignment_table import cluster_assignment
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_cluster_assignment, {})
del(one_data_got_by_parent['cluster'])
one_data_updated = merge_dicts(ad.add_one_cluster_assignment, {})
one_data_updated['name'] = 'sample3'

# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    cluster.add_one(ad.add_one_cluster)


def add_parents_tsv(client):
    client.post('/api/dataset/add',
        data=json.dumps(ad.add_one_dataset), headers=ad.json_headers)
    client.post('/api/clustering_solution/add',
        data=json.dumps(ad.add_one_clustering_solution),
        headers=ad.json_headers)
    client.post('/api/cluster/add',
        data=json.dumps(ad.add_one_cluster),
        headers=ad.json_headers)


def test_add_one(app):
    with app.app_context():
        add_parents()
        result = cluster_assignment.add_one(ad.add_one_cluster_assignment)
        assert result == None
        result = cluster_assignment.get_one('sample1', ad.accept_json)
        assert dicts_equal(result, ad.add_one_cluster_assignment)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = cluster_assignment.add_one(ad.add_one_cluster_assignment)
        assert result == '404 Parent not found: cluster: cluster1'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        cluster_assignment.add_one(ad.add_one_cluster_assignment)
        result = cluster_assignment.get_by_parent('cluster1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got_by_parent)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        cluster_assignment.add_one(ad.add_one_cluster_assignment)
        result = cluster_assignment.get_by_parent('clusterX', ad.accept_json)
        assert result == '404 Parent not found: cluster: clusterX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        cluster_assignment.add_one(ad.add_one_cluster_assignment)
        result = cluster_assignment.get_one('sample1', ad.accept_json)
        assert dicts_equal(result, ad.add_one_cluster_assignment)


def test_json_api(client):
    # add one
    add_parents_tsv(client)
    response = client.post('/api/cluster_assignment/add',
        data=json.dumps(ad.add_one_cluster_assignment),
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert response.json == None

    # get one
    response = client.get('/api/cluster_assignment/sample1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json, ad.add_one_cluster_assignment)

    # get by parent
    response = client.get(
        '/api/cluster_assignment/get_by_cluster/cluster1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], one_data_got_by_parent)

    # update
    response = client.get('/api/cluster_assignment/update/name/' + \
        'sample1/field/name/value/sample3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/cluster_assignment/sample3',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    print('response.json:', response.json)
    assert dicts_equal(response.json, one_data_updated)

    # delete
    response = client.get('/api/cluster_assignment/delete/sample3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/cluster_assignment/sample3')
    assert response.json == '404 Not found: cluster_assignment: sample3'


def test_tsv_api(client):
    # add many tsv
    add_parents_tsv(client)
    response = client.get('/api/cluster_assignment/add_many/tsv_file/' + \
        'cluster_assignment.tsv/cluster/cluster1')

    assert response.content_type == ad.accept_json
    assert response.data.decode("utf-8") == 'null\n'

    # get one
    response = client.get('/api/cluster_assignment/cluster_assignment1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
        'name\tcluster\ncluster_assignment1\tcluster1'

    # get by parent
    response = client.get('/api/cluster_assignment/get_by_cluster/cluster1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name
cluster_assignment1
cluster_assignment2'''

    # update
    response = client.get('/api/cluster_assignment/update/name' + \
        '/cluster_assignment1/field/name/value/cluster_assignment3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/cluster_assignment/cluster_assignment3',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	cluster
cluster_assignment3	cluster1'''

    # delete
    response = client.get(
        '/api/cluster_assignment/delete/cluster_assignment3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/cluster_assignment/cluster_assignment3',
        headers=ad.tsv_headers)
    assert response.data.decode("utf-8") == \
        '404 Not found: cluster_assignment: cluster_assignment3'


