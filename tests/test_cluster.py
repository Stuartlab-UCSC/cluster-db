
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest, json
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.attribute_table import attribute
from cluster.database.cluster_assignment_table import cluster_assignment
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_cluster, {})
del(one_data_got_by_parent['clustering_solution'])
one_data_updated = merge_dicts(ad.add_one_cluster, {})
one_data_updated['name'] = 'cluster3'
second_data_got_by_parent = merge_dicts(ad.add_second_cluster, {})
del(second_data_got_by_parent['clustering_solution'])


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)


def test_add_two_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        result = cluster.add_one(ad.add_one_cluster, ['dataset1'])
        assert result == 1
        result = cluster.add_one(ad.add_second_cluster, ['dataset1'])
        assert result == 2
        result = cluster.get_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
'''name
cluster1
cluster2'''


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv(
            'cluster.tsv', ['clustering_solution1', 'dataset1'])
        assert result == 2
        result = cluster.get_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
'''name
cluster1
cluster2'''

"""
def test_delete_has_children_attribute(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        attribute.add_one(ad.add_one_attribute)
        result = cluster.delete('cluster1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_delete_has_children_cluster_assignment(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        cluster_assignment.add_one(ad.add_one_cluster_assignment)
        result = cluster.delete('cluster1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'

"""

def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv(
            'cluster.tsv', ['clustering_solution1', 'dataset1'])
        result = cluster.get_by_parent(['clustering_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: clustering_solution: clustering_solutionX'


def test_api_tsv(client, app):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get('/api/cluster/add' + \
            '/tsv_file/cluster.tsv' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'

        # get by parent
        response = client.get(
            '/api/cluster/get_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name
cluster1
cluster2'''

    """
    # update
    response = client.get('/api/cluster/update/name' + \
        '/cluster1/field/name/value/cluster3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/cluster/cluster3')
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	clustering_solution
cluster3	clustering_solution1'''

    # delete
    response = client.get(
        '/api/cluster/delete/cluster3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/cluster/cluster3')
    assert response.data.decode("utf-8") == \
        '404 Not found: cluster: cluster3'
    """

