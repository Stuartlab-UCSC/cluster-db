
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

second_data_got_by_parent = merge_dicts(ad.add_second_cluster_assignment, {})
del(second_data_got_by_parent['cluster'])

# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(
        ad.add_one_clustering_solution, ['dataset1'])
    cluster.add_one(ad.add_one_cluster, ['clustering_solution1', 'dataset1'])


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        result = cluster_assignment.add_tsv('cluster_assignment.tsv',
            ['cluster1', 'clustering_solution1', 'dataset1'])
        assert result == None
        result = cluster_assignment.get_by_parent(
            ['cluster1', 'clustering_solution1', 'dataset1'], ad.accept_json)
        assert dicts_equal(result[0], one_data_got_by_parent)
        assert dicts_equal(result[1], second_data_got_by_parent)

def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        result = cluster_assignment.add_tsv('cluster_assignment.tsv',
            ['cluster1', 'clustering_solution1', 'dataset1'])
        result = cluster_assignment.get_by_parent(
            ['clusterX', 'clustering_solution1', 'dataset1'], ad.accept_json)
        assert result == '404 Parent not found: cluster: clusterX'

def test_tsv_api(app, client):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get(
            '/api/cluster_assignment/add' + \
            '/tsv_file/cluster_assignment.tsv' + \
            '/cluster/cluster1' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        print('response.data:', response.data)
        assert response.content_type == ad.accept_json
        assert response.data.decode("utf-8") == 'null\n'

        # get by parent
        response = client.get(
            '/api/cluster_assignment/get_by' + \
            '/cluster/cluster1' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1',
             headers=ad.tsv_headers)
        assert response.content_type == ad.accept_tsv
        assert response.data.decode("utf-8") == \
'''name
sample1
sample2'''
        """
        # update
        response = client.get('/api/cluster_assignment/update/name' + \
            '/cluster_assignment/field/name/value/cluster_assignment3')
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
        """

def test_json_api(app, client):
    with app.app_context():
        # get by parent
        add_parents()
        client.get(
            '/api/cluster_assignment/add' + \
            '/tsv_file/cluster_assignment.tsv' + \
            '/cluster/cluster1' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        response = client.get(
            '/api/cluster_assignment/get_by' + \
            '/cluster/cluster1' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1',
             headers=ad.json_headers)
        print('response.json:', response.json)
        print('one_data_got_by_parent:', one_data_got_by_parent)
        assert response.content_type == ad.accept_json
        assert dicts_equal(response.json[0], one_data_got_by_parent)
        assert dicts_equal(response.json[1], second_data_got_by_parent)
        """
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
        """

