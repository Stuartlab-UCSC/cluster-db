
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.attribute_table import attribute
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


def test_db(app):
    with app.app_context():
        add_parents()
        result = attribute.add_tsv(
            'attribute.tsv', ['clustering_solution1', 'dataset1'])
        assert result == 4
        result = attribute.add_tsv(
            'attribute.tsv', ['clustering_solution2', 'dataset1'])
        assert result == 8
        result = attribute.add_tsv(
            'attribute.tsv', ['clustering_solution2', 'dataset2'])
        assert result == 12

        # verify adds
        result = attribute.get_all()
        print('result', result)
        assert result == \
'''name	value	cluster_id
attribute1	value11	1
attribute2	value21	1
attribute1	value12	2
attribute2	value22	2
attribute1	value11	3
attribute2	value21	3
attribute1	value12	4
attribute2	value22	4
attribute1	value11	5
attribute2	value21	5
attribute1	value12	6
attribute2	value22	6'''

        # get by clustering_solution
        result = attribute.get_by_clustering_solution_clusters(
            ['clustering_solution1', 'dataset1'])
        #print('result:', result)
        assert result == \
'''name	value	cluster
attribute1	value11	cluster1
attribute2	value21	cluster1
attribute1	value12	cluster2
attribute2	value22	cluster2'''

        # delete for one clustering_solution
        result = attribute.delete_by_clustering_solution_clusters(
            ['clustering_solution1', 'dataset1'])
        #print('result:', result)
        assert result == ''


        # verify delete
        result = attribute.get_all()
        print('result', result)
        assert result == \
'''name	value	cluster_id
attribute1	value11	3
attribute2	value21	3
attribute1	value12	4
attribute2	value22	4
attribute1	value11	5
attribute2	value21	5
attribute1	value12	6
attribute2	value22	6'''


def test_get_by_clustering_solution_clustering_solution_not_found(app):
    with app.app_context():
        add_parents()
        attribute.add_tsv(
            'attribute.tsv', ['clustering_solution1', 'dataset1'])
        result = attribute.get_by_parent(
            ['clustering_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(app, client):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get(
            '/api/attribute/add' + \
            '/tsv_file/attribute.tsv' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        print('response.data:',  response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/api/attribute/add' + \
            '/tsv_file/attribute.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '8'
        response = client.get(
            '/api/attribute/add' + \
            '/tsv_file/attribute.tsv' + \
            '/clustering_solution/clustering_solution2' + \
            '/dataset/dataset2')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '12'

        # verify adds.
        response = client.get('/api/attribute')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster_id
attribute1	value11	1
attribute2	value21	1
attribute1	value12	2
attribute2	value22	2
attribute1	value11	3
attribute2	value21	3
attribute1	value12	4
attribute2	value22	4
attribute1	value11	5
attribute2	value21	5
attribute1	value12	6
attribute2	value22	6'''

        # get by parent
        response = client.get(
            '/api/attribute/get_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        print('response.json:', response.json)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster
attribute1	value11	cluster1
attribute2	value21	cluster1
attribute1	value12	cluster2
attribute2	value22	cluster2'''

        # delete
        response = client.get(
            '/api/attribute/delete_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == ''
        
        
        # verify delete
        response = client.get('/api/attribute')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	value	cluster_id
attribute1	value11	3
attribute2	value21	3
attribute1	value12	4
attribute2	value22	4
attribute1	value11	5
attribute2	value21	5
attribute1	value12	6
attribute2	value22	6'''
