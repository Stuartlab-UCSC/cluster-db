
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import pytest, json
import tests.access_db_data as ad
from cluster.database_update.dataset_table import dataset
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_attribute_table import cluster_attribute
from cluster.database_update.cell_of_cluster_table import cell_of_cluster
from cluster.database.db import dicts_equal, merge_dicts


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster_solution.add_one(ad.add_second_cluster_solution)
    cluster_solution.add_one(ad.add_third_cluster_solution)


def test_db(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['cluster_solution1', 'dataset1'])
        assert result == 2
        result = cluster.add_tsv('cluster.tsv',
            ['cluster_solution2', 'dataset1'])
        assert result == 4
        result = cluster.add_tsv('cluster.tsv',
            ['cluster_solution2', 'dataset2'])
        assert result == 6
    
        # verify adds
        result = cluster.get_all()
        #print('result:', result)
        assert result == \
'''name	label	description	cluster_solution_id
cluster1	label1	description1	1
cluster2	label2	description2	1
cluster1	label1	description1	2
cluster2	label2	description2	2
cluster1	label1	description1	3
cluster2	label2	description2	3'''
    
        # get by parent
        result = cluster.get_by_parent(['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result == \
'''name	label	description
cluster1	label1	description1
cluster2	label2	description2'''

        # delete
        result = cluster.delete_by_parent(
        	['cluster_solution2', 'dataset1'])
        #print('result:', result)
        assert result == None
    
        # verify delete
        result = cluster.get_all()
        print('result:', result)
        assert result == \
'''name	label	description	cluster_solution_id
cluster1	label1	description1	1
cluster2	label2	description2	1
cluster1	label1	description1	3
cluster2	label2	description2	3'''


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv(
            'cluster.tsv', ['cluster_solution1', 'dataset1'])
        assert result == 2
        result = cluster.get_by_parent(
            ['cluster_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
'''name	label	description
cluster1	label1	description1
cluster2	label2	description2'''

def test_delete_has_children_cluster_attribute(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['cluster_solution1', 'dataset1'])
        assert result == 2
        result = cluster_attribute.add_tsv('cluster_attribute.tsv',
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result == 4
        result = cluster.delete_by_parent(
            ['cluster_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
            '400 There are children that would be orphaned, delete those first'

def test_delete_has_children_cell_of_cluster(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv('cluster.tsv',
            ['cluster_solution1', 'dataset1'])
        assert result == 2
        result = cell_of_cluster.add_tsv('cell_of_cluster.tsv',
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result == 4
        result = cluster.delete_by_parent(
            ['cluster_solution1', 'dataset1'])
        print('result:', result)
        assert result == \
            '400 There are children that would be orphaned, delete those first'

def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        result = cluster.add_tsv(
            'cluster.tsv', ['cluster_solution1', 'dataset1'])
        result = cluster.get_by_parent(['cluster_solutionX', 'dataset1'])
        assert result == '404 Not found: parent'


def test_api(client, app):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get('/cluster-update/add' + \
            '/tsv_file/cluster.tsv' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'
        response = client.get('/cluster-update/add' + \
            '/tsv_file/cluster.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get('/cluster-update/add' + \
            '/tsv_file/cluster.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '6'

        # verify adds
        response = client.get('/cluster-update')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	label	description	cluster_solution_id
cluster1	label1	description1	1
cluster2	label2	description2	1
cluster1	label1	description1	2
cluster2	label2	description2	2
cluster1	label1	description1	3
cluster2	label2	description2	3'''

        # get by parent
        response = client.get(
            '/cluster-update/get_by' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	label	description
cluster1	label1	description1
cluster2	label2	description2'''

        # delete
        response = client.get(
            '/cluster-update/delete_by' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.data.decode("utf-8") == 'None'

        # verify delete
        response = client.get('/cluster-update')
        print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	label	description	cluster_solution_id
cluster1	label1	description1	1
cluster2	label2	description2	1
cluster1	label1	description1	3
cluster2	label2	description2	3'''

