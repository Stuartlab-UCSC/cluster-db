
# We don't duplicate tests aready done for common code in test_dataset.py.

import pytest, json
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.cluster_table import cluster
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_clustering_solution, {})
one_data_got_all = merge_dicts(ad.add_one_clustering_solution, {})
del(one_data_got_by_parent['dataset'])
one_data_updated = merge_dicts(ad.add_one_clustering_solution, {})
one_data_updated['name'] = 'clustering_solution3'
second_data_got_by_parent = merge_dicts(ad.add_second_clustering_solution, {})
del(second_data_got_by_parent['dataset'])


def add_parent():
    dataset.add_one(ad.add_one_dataset)


def test_add_one_and_get_by_parent(app):
    with app.app_context():
        add_parent()
        result = clustering_solution.add_one(
            ad.add_one_clustering_solution, ['dataset1'])
        assert result == None
        result = clustering_solution.add_one(
            ad.add_second_clustering_solution, ['dataset1'])
        assert result == None
        result = clustering_solution.get_by_parent(['dataset1'], ad.accept_json)
        assert dicts_equal(result[0], one_data_got_by_parent)
        assert dicts_equal(result[1], second_data_got_by_parent)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = clustering_solution.add_one(
            ad.add_one_clustering_solution, ['dataset1'])
        assert result == '404 Not found: dataset: dataset1'

"""
def test_delete(app):
    with app.app_context():
        add_parent()
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.delete(
            'clustering_solution1', ['dataset1'])
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', ad.accept_json)
        assert result == \
            '404 Not found: clustering_solution: clustering_solution1'


def test_delete_not_found(app):
    with app.app_context():
        add_parent()
        result = clustering_solution.delete(
            'clustering_solution1', ['dataset1'])
        assert result == \
            '404 Not found: clustering_solution: clustering_solution1'
"""
"""
# TODO test after child code is there.
def test_delete_has_children_signature_gene_set(app):
    with app.app_context():
        add_parent()
        clustering_solution.add_one(ad.add_one_clustering_solution)
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = clustering_solution.delete(
            'clustering_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_delete_has_children_cluster(app):
    with app.app_context():
        add_parent()
        clustering_solution.add_one(ad.add_one_clustering_solution)
        cluster.add_one(ad.add_one_cluster)
        result = clustering_solution.delete(
            'clustering_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'
"""

def test_get_by_parent_one_tsv(app):
    with app.app_context():
        add_parent()
        clustering_solution.add_one(
            ad.add_one_clustering_solution, ['dataset1'])
        result = clustering_solution.get_by_parent(['dataset1'], ad.accept_tsv)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0'''


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        add_parent()
        result = clustering_solution.get_by_parent(['dataset1'], ad.accept_json)
        assert result == \
            '404 Not found: clustering_solution with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parent()
        clustering_solution.add_one(
            ad.add_one_clustering_solution, ['dataset1'])
        result = clustering_solution.get_by_parent(['datasetX'], ad.accept_json)
        assert result == '404 Not found: dataset: datasetX'


def test_tsv_api(app, client):
    with app.app_context():
        # add tsv
        add_parent()
        response = client.get(
            '/api/clustering_solution/add' + \
            '/tsv_file/clustering_solution.tsv' + \
            '/dataset/dataset1')
        assert response.content_type == ad.accept_json
        assert response.json == None
        """
        # get all
        response = client.get('/api/clustering_solution', headers=ad.json_headers)
        print('response.data:', response.data)
        assert False
        """
        # get by parent
        response = client.get(
            '/api/clustering_solution/get_by/dataset/dataset1',
            headers=ad.tsv_headers)
        assert response.content_type == ad.accept_tsv
        assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0
clustering_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1'''
        """
        # update
        response = client.get('/api/clustering_solution/update/name' + \
            '/clustering_solution1/field/name/value/clustering_solution3')
        assert response.data == b'null\n'
        # check that it was updated
        response = client.get('/api/clustering_solution/clustering_solution3', headers=ad.tsv_headers)
        assert response.content_type == ad.accept_tsv
        assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary	dataset
clustering_solution3	method1	method_implementation1	method_url1	method_parameters1	analyst1	0	dataset1'''

        # delete
        response = client.get(
            '/api/clustering_solution/delete/clustering_solution3')
        assert response.data == b'null\n'
        # check that it was really deleted
        response = client.get('/api/clustering_solution/clustering_solution3',
            headers=ad.tsv_headers)
        assert response.data.decode("utf-8") == \
            '404 Not found: clustering_solution: clustering_solution3'
        """

def test_json_api(app, client):
    with app.app_context():
        # get by parent
        add_parent()
        response = client.get(
            '/api/clustering_solution/add' + \
            '/tsv_file/clustering_solution.tsv' + \
            '/dataset/dataset1')
        response = client.get(
            '/api/clustering_solution/get_by/dataset/dataset1',
            headers=ad.json_headers)
        assert response.content_type == ad.accept_json
        print('response.json', response.json)
        print('one_data_got_by_parent', one_data_got_by_parent)
        assert dicts_equal(response.json[0], one_data_got_by_parent)
        """
        # update
        response = client.get('/api/clustering_solution/update/name' + \
            '/clustering_solution1/field/name/value/clustering_solution3')
        assert response.data == b'null\n'
        # check that it was updated
        response = client.get('/api/clustering_solution/clustering_solution3',
            headers=ad.json_headers)
        assert response.content_type == ad.accept_json
        assert dicts_equal(response.json, one_data_updated)

        # delete
        response = client.get(
            '/api/clustering_solution/delete/clustering_solution3')
        assert response.data == b'null\n'
        # check that it was really deleted
        response = client.get('/api/clustering_solution/clustering_solution3')
        assert response.json == \
            '404 Not found: clustering_solution: clustering_solution3'
        print('response.json:',response.json[0])
        print('     expected:',one_data_got_by_parent)
        """
