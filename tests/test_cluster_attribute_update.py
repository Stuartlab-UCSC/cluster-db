
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database_update.dataset_table import dataset
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_attribute_table import cluster_attribute
from cluster.database.db_old import dicts_equal, merge_dicts

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


def test_db(app):
    with app.app_context():
        add_parents()
        result = cluster_attribute.add_tsv(
            'cluster_attribute.tsv', ['cluster_solution1', 'dataset1'])
        assert result == 4
        result = cluster_attribute.add_tsv(
            'cluster_attribute.tsv', ['cluster_solution2', 'dataset1'])
        assert result == 8
        result = cluster_attribute.add_tsv(
            'cluster_attribute.tsv', ['cluster_solution2', 'dataset2'])
        assert result == 12

        # verify adds
        result = cluster_attribute.get_all()
        print('result', result)
        assert result == \
'''name	value	cluster_id
cluster_attribute1	value11	1
cluster_attribute2	value21	1
cluster_attribute1	value12	2
cluster_attribute2	value22	2
cluster_attribute1	value11	3
cluster_attribute2	value21	3
cluster_attribute1	value12	4
cluster_attribute2	value22	4
cluster_attribute1	value11	5
cluster_attribute2	value21	5
cluster_attribute1	value12	6
cluster_attribute2	value22	6'''

        # get by cluster_solution
        result = cluster_attribute.get_by_cluster_solution_clusters(
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result == \
'''name	value	cluster
cluster_attribute1	value11	cluster1
cluster_attribute2	value21	cluster1
cluster_attribute1	value12	cluster2
cluster_attribute2	value22	cluster2'''

        # delete for one cluster_solution
        result = cluster_attribute.delete_by_cluster_solution_clusters(
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result == ''


        # verify delete
        result = cluster_attribute.get_all()
        print('result', result)
        assert result == \
'''name	value	cluster_id
cluster_attribute1	value11	3
cluster_attribute2	value21	3
cluster_attribute1	value12	4
cluster_attribute2	value22	4
cluster_attribute1	value11	5
cluster_attribute2	value21	5
cluster_attribute1	value12	6
cluster_attribute2	value22	6'''


def test_get_by_cluster_solution_cluster_solution_not_found(app):
    with app.app_context():
        add_parents()
        cluster_attribute.add_tsv(
            'cluster_attribute.tsv', ['cluster_solution1', 'dataset1'])
        result = cluster_attribute.get_by_parent(
            ['cluster_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(app, client):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get(
            '/cluster-attribute-update/add' + \
            '/tsv_file/cluster_attribute.tsv' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        print('response.data:',  response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/cluster-attribute-update/add' + \
            '/tsv_file/cluster_attribute.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '8'
        response = client.get(
            '/cluster-attribute-update/add' + \
            '/tsv_file/cluster_attribute.tsv' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '12'

        # verify adds.
        response = client.get('/cluster-attribute-update')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster_id
cluster_attribute1	value11	1
cluster_attribute2	value21	1
cluster_attribute1	value12	2
cluster_attribute2	value22	2
cluster_attribute1	value11	3
cluster_attribute2	value21	3
cluster_attribute1	value12	4
cluster_attribute2	value22	4
cluster_attribute1	value11	5
cluster_attribute2	value21	5
cluster_attribute1	value12	6
cluster_attribute2	value22	6'''

        # get by parent
        response = client.get(
            '/cluster-attribute-update/get_by' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        print('response.json:', response.json)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster
cluster_attribute1	value11	cluster1
cluster_attribute2	value21	cluster1
cluster_attribute1	value12	cluster2
cluster_attribute2	value22	cluster2'''

        # delete
        response = client.get(
            '/cluster-attribute-update/delete_by' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == ''
        
        
        # verify delete
        response = client.get('/cluster-attribute-update')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster_id
cluster_attribute1	value11	3
cluster_attribute2	value21	3
cluster_attribute1	value12	4
cluster_attribute2	value22	4
cluster_attribute1	value11	5
cluster_attribute2	value21	5
cluster_attribute1	value12	6
cluster_attribute2	value22	6'''
