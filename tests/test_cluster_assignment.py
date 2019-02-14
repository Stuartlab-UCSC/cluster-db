
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


# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    clustering_solution.add_one(ad.add_second_clustering_solution)
    clustering_solution.add_one(ad.add_third_clustering_solution)
    cluster.add_tsv('cluster.tsv', ['clustering_solution1', 'dataset1'])
    cluster.add_tsv('cluster.tsv', ['clustering_solution2', 'dataset1'])
    cluster.add_tsv('cluster.tsv', ['clustering_solution2', 'dataset2'])


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        
        # add three sets of assignments
        result = cluster_assignment.add_tsv(
            'cluster_assignment.tsv', ['clustering_solution1', 'dataset1'])
        assert result == 4
        result = cluster_assignment.add_tsv(
            'cluster_assignment.tsv', ['clustering_solution2', 'dataset1'])
        assert result == 8
        result = cluster_assignment.add_tsv(
            'cluster_assignment.tsv', ['clustering_solution2', 'dataset2'])
        assert result == 12

        # verify adds
        result = cluster_assignment.get_all()
        print('result', result)
        assert result == \
'''name	cluster_id
sample1	1
sample2	2
sample3	1
sample4	2
sample1	3
sample2	4
sample3	3
sample4	4
sample1	5
sample2	6
sample3	5
sample4	6'''

        # get by clustering solution
        result = cluster_assignment.get_by_clustering_solution_clusters(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
'''name	cluster
sample1	cluster1
sample3	cluster1
sample2	cluster2
sample4	cluster2'''


        # delete
        result = cluster_assignment.delete_by_clustering_solution_clusters(
            ['clustering_solution2', 'dataset1'])
        print('result:', result)
        assert result == ''
        
        # verify delete
        result = cluster_assignment.get_all()
        print('result', result)
        assert result == \
'''name	cluster_id
sample1	1
sample2	2
sample3	1
sample4	2
sample1	5
sample2	6
sample3	5
sample4	6'''


def test_get_by_clustering_solution_clustering_solution_not_found(app):
    with app.app_context():
        add_parents()
        result = cluster_assignment.get_by_parent(
            ['clustering_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(app, client):
    with app.app_context():
        add_parents()
        
        # add three sets of assignments
        response = client.get(
            '/api/cluster_assignment/add' + \
            '/tsv_file/cluster_assignment.tsv' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/api/cluster_assignment/add' + \
            '/tsv_file/cluster_assignment.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '8'
        response = client.get(
            '/api/cluster_assignment/add' + \
            '/tsv_file/cluster_assignment.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '12'
        
        # verify adds
        response = client.get('/api/cluster_assignment')
        print('response.data:', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	cluster_id
sample1	1
sample2	2
sample3	1
sample4	2
sample1	3
sample2	4
sample3	3
sample4	4
sample1	5
sample2	6
sample3	5
sample4	6'''

        # get by parent
        response = client.get(
            '/api/cluster_assignment/get_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	cluster
sample1	cluster1
sample3	cluster1
sample2	cluster2
sample4	cluster2'''

        # delete
        response = client.get( \
            '/api/cluster_assignment/delete_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.data.decode("utf-8") == ''

        # verify delete
        # verify adds
        response = client.get('/api/cluster_assignment')
'''name	cluster_id
sample1	3
sample2	4
sample3	3
sample4	4
sample1	5
sample2	6
sample3	5
sample4	6'''
