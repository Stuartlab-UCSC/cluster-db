
# We don't duplicate tests aready done for common code in test_dataset.py.

import pytest, json
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.cluster_table import cluster
from cluster.database.db import dicts_equal, merge_dicts


def add_parent():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)


def test_add_three_and_get_by_parent(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.add_one(
            ad.add_one_cluster_solution)
        assert result == 1
        result = cluster_solution.add_one(
            ad.add_second_cluster_solution)
        assert result == 2
        result = cluster_solution.add_one(
            ad.add_third_cluster_solution)
        assert result == 3

        #result = cluster_solution.get_all()
        #print('result:', result)
        #assert false

		# verify first two adds.
        result = cluster_solution.get_by_parent(['dataset1'])
        #print('result:', result)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
cluster_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0
cluster_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1'''

		# verify last add
        result = cluster_solution.get_by_parent(['dataset2'])
        print('result:', result)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
cluster_solution2	method3	method_implementation3	method_url3	method_parameters3	analyst3	1'''

        # delete what doesn't exist
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == None
        
        # verify deleted nothing
        result = cluster_solution.get_all()
        print('result:', result)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary	dataset_id
cluster_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1	1
cluster_solution2	method3	method_implementation3	method_url3	method_parameters3	analyst3	1	2'''


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = cluster_solution.add_one(
            ad.add_one_cluster_solution)
        assert result == '404 Not found: parent'


def test_delete_not_found(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == '404 Not found: cluster_solution: cluster_solution1'


def test_delete_has_children_signature_gene_set(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        signature_gene_set.add_tsv('signature_gene_set.tsv',
            ['cluster_solution1', 'dataset1'])
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_delete_has_children_cluster(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        cluster.add_tsv('cluster.tsv', ['cluster_solution1', 'dataset1'])
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.get_by_parent(['dataset1'])
        assert result == \
            '404 Not found: cluster_solution with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        result = cluster_solution.get_by_parent(['datasetX'])
        assert result == '404 Not found: parent'


def test_api_add_one_and_get_by_parent(app, client):
    # add one
    with app.app_context():
        add_parent()
        response = ad.post_json(
            client, '/api/cluster_solution/add', ad.add_one_cluster_solution)
        response = ad.post_json(
            client, '/api/cluster_solution/add', ad.add_third_cluster_solution)
        #print('response', response)
        #print('response.decode', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain

        # get by parent
        response = client.get(
            '/api/cluster_solution/get_by/dataset/dataset1')
        assert response.content_type == ad.text_plain
        #print('response.data:', response.data)
        #print('response.decode', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
cluster_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0'''

        # delete
        response = client.get(
            '/api/cluster_solution' +
            '/delete/cluster_solution1' +
            '/dataset/dataset1')
        print('response.data:', response.data)
        print('response.decode', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain

        # verify delete
        response = client.get(
            '/api/cluster_solution/get_by/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
        	'404 Not found: cluster_solution with dataset: dataset1'
        
        # verify delete did not delete another
        response = client.get(
            '/api/cluster_solution/get_by/dataset/dataset2')
        assert response.content_type == ad.text_plain
        print('response.data:', response.data)
        assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
cluster_solution2	method3	method_implementation3	method_url3	method_parameters3	analyst3	1'''


def test_api_tsv(app, client):
    with app.app_context():
        # add tsv
        add_parent()
        response = client.get(
            '/api/cluster_solution/add' + \
            '/tsv_file/cluster_solution.tsv' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'

        # get by parent
        response = client.get(
            '/api/cluster_solution/get_by/dataset/dataset1')
        assert response.content_type == ad.text_plain
        print('response.data:', response.data)
        assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
cluster_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0
cluster_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1'''

