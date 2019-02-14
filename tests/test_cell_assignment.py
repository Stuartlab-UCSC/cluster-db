
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.cluster_table import cluster
from cluster.database.cell_assignment_table import cell_assignment
from cluster.database.db import dicts_equal, merge_dicts


# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster_solution.add_one(ad.add_second_cluster_solution)
    cluster_solution.add_one(ad.add_third_cluster_solution)
    cluster.add_tsv('cluster.tsv', ['cluster_solution1', 'dataset1'])
    cluster.add_tsv('cluster.tsv', ['cluster_solution2', 'dataset1'])
    cluster.add_tsv('cluster.tsv', ['cluster_solution2', 'dataset2'])


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        
        # add three sets of assignments
        result = cell_assignment.add_tsv(
            'cell_assignment.tsv', ['cluster_solution1', 'dataset1'])
        assert result == 4
        result = cell_assignment.add_tsv(
            'cell_assignment.tsv', ['cluster_solution2', 'dataset1'])
        assert result == 8
        result = cell_assignment.add_tsv(
            'cell_assignment.tsv', ['cluster_solution2', 'dataset2'])
        assert result == 12

        # verify adds
        result = cell_assignment.get_all()
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

        # get by cluster solution
        result = cell_assignment.get_by_cluster_solution_clusters(
            ['cluster_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
'''name	cluster
sample1	cluster1
sample3	cluster1
sample2	cluster2
sample4	cluster2'''


        # delete
        result = cell_assignment.delete_by_cluster_solution_clusters(
            ['cluster_solution2', 'dataset1'])
        print('result:', result)
        assert result == ''
        
        # verify delete
        result = cell_assignment.get_all()
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


def test_get_by_cluster_solution_cluster_solution_not_found(app):
    with app.app_context():
        add_parents()
        result = cell_assignment.get_by_parent(
            ['cluster_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(app, client):
    with app.app_context():
        add_parents()
        
        # add three sets of assignments
        response = client.get(
            '/api/cell_assignment/add' + \
            '/tsv_file/cell_assignment.tsv' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/api/cell_assignment/add' + \
            '/tsv_file/cell_assignment.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '8'
        response = client.get(
            '/api/cell_assignment/add' + \
            '/tsv_file/cell_assignment.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '12'
        
        # verify adds
        response = client.get('/api/cell_assignment')
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
            '/api/cell_assignment/get_by' + \
            '/cluster_solution/cluster_solution1' + \
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
            '/api/cell_assignment/delete_by' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.data.decode("utf-8") == ''

        # verify delete
        # verify adds
        response = client.get('/api/cell_assignment')
'''name	cluster_id
sample1	3
sample2	4
sample3	3
sample4	4
sample1	5
sample2	6
sample3	5
sample4	6'''
