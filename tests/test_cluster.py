
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


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    clustering_solution.add_one(ad.add_second_clustering_solution)
    clustering_solution.add_one(ad.add_third_clustering_solution)


def test_db(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['clustering_solution1', 'dataset1'])
        assert result == 2
        result = cluster.add_tsv('cluster.tsv',
            ['clustering_solution2', 'dataset1'])
        assert result == 4
        result = cluster.add_tsv('cluster.tsv',
            ['clustering_solution2', 'dataset2'])
        assert result == 6
    
        # verify adds
        result = cluster.get_all()
        #print('result:', result)
        assert result == \
'''name	clustering_solution_id
cluster1	1
cluster2	1
cluster1	2
cluster2	2
cluster1	3
cluster2	3'''
    
        # get by parent
        result = cluster.get_by_parent(['clustering_solution1', 'dataset1'])
        #print('result:', result)
        assert result == \
'''name
cluster1
cluster2'''
    
        # delete
        result = cluster.delete_by_parent(
        	['clustering_solution2', 'dataset1'])
        #print('result:', result)
        assert result == None
    
        # verify delete
        result = cluster.get_all()
        print('result:', result)
        assert result == \
'''name	clustering_solution_id
cluster1	1
cluster2	1
cluster1	3
cluster2	3'''


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

def test_delete_has_children_attribute(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['clustering_solution1', 'dataset1'])
        assert result == 2
        result = attribute.add_tsv('attribute.tsv',
            ['clustering_solution1', 'dataset1'])
        #print('result:', result)
        assert result == 4
        result = cluster.delete_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
            '400 There are children that would be orphaned, delete those first'

def test_delete_has_children_cluster_assignment(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['clustering_solution1', 'dataset1'])
        assert result == 2
        result = cluster_assignment.add_tsv('cluster_assignment.tsv',
            ['clustering_solution1', 'dataset1'])
        #print('result:', result)
        assert result == 4
        result = cluster.delete_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
            '400 There are children that would be orphaned, delete those first'

def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv(
            'cluster.tsv', ['clustering_solution1', 'dataset1'])
        result = cluster.get_by_parent(['clustering_solutionX', 'dataset1'])
        assert result == '404 Not found: parent'


def test_api(client, app):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get('/api/cluster/add' + \
            '/tsv_file/cluster.tsv' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'
        response = client.get('/api/cluster/add' + \
            '/tsv_file/cluster.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get('/api/cluster/add' + \
            '/tsv_file/cluster.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '6'

        # verify adds
        response = client.get('/api/cluster')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	clustering_solution_id
cluster1	1
cluster2	1
cluster1	2
cluster2	2
cluster1	3
cluster2	3'''

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

        # delete
        response = client.get(
            '/api/cluster/delete_by' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset1')
        assert response.data.decode("utf-8") == 'None'

        # verify delete
        response = client.get('/api/cluster')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	clustering_solution_id
cluster1	1
cluster2	1
cluster1	3
cluster2	3'''

