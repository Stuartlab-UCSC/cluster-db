
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_signature_gene_set, {})
del(one_data_got_by_parent['clustering_solution'])
one_data_updated = merge_dicts(ad.add_one_signature_gene_set, {})
one_data_updated['name'] = 'signature_gene_set3'
second_data_got_by_parent = merge_dicts(ad.add_second_signature_gene_set, {})
del(second_data_got_by_parent['clustering_solution'])


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)

def test_add_two(app):
    with app.app_context():
        add_parents()
        result = signature_gene_set.add_one(
            ad.add_one_signature_gene_set, ['dataset1'])
        result = signature_gene_set.add_one(
            ad.add_second_signature_gene_set, ['dataset1'])
        assert result == 2
        result = signature_gene_set.get_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result ==  \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''


def test_add_tsv(app):
    with app.app_context():
        add_parents()
        result = signature_gene_set.add_tsv(
            'signature_gene_set.tsv', ['clustering_solution1', 'dataset1'])
        assert result == 2
        result = signature_gene_set.get_by_parent(
            ['clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result ==  \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_tsv(
            'signature_gene_set.tsv', ['clustering_solution1', 'dataset1'])
        result = signature_gene_set.get_by_parent(
            ['clustering_solutionX', 'dataset1'])
        assert result == \
            '404 Not found: clustering_solution: clustering_solutionX'


"""
def test_delete_has_children(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene_set.delete('signature_gene_set1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'
"""


def test_api_add_one_and_get_by_parent(client):
    # add one
    add_parents()
    response = ad.post_json(
        client, '/api/signature_gene_set/add_by/dataset/dataset1',
        ad.add_one_signature_gene_set)
    print('response.data', response.data)
    #assert response.content_type == ad.text_plain
    response = ad.post_json(
        client, '/api/signature_gene_set/add_by/dataset/dataset1',
        ad.add_second_signature_gene_set)
    #assert response.content_type == ad.text_plain
    print('response.data', response.data)
    assert response.data.decode("utf-8") == '2'

    # get by parent
    response = client.get(
        '/api/signature_gene_set/get_by' + \
        '/clustering_solution/clustering_solution1' + \
        '/dataset/dataset1')
    print('response.data:', response.data)
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''


def test_api_tsv(app, client):
    with app.app_context():
        # add many tsv
        add_parents()
        response = client.get(
            '/api/signature_gene_set/add' + \
            '/tsv_file/signature_gene_set.tsv' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'

        # get by parent
        response = client.get(
            '/api/signature_gene_set/get_by' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        print('response.data:', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''

"""
    # update
    response = client.get('/api/signature_gene_set/update/name' + \
        '/signature_gene_set1/field/name/value/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/signature_gene_set/signature_gene_set3')
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	method	clustering_solution
signature_gene_set3	method1	clustering_solution1'''

    # delete
    response = client.get(
        '/api/signature_gene_set/delete/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/signature_gene_set/signature_gene_set3')
    assert response.data.decode("utf-8") == \
        '404 Not found: signature_gene_set: signature_gene_set3'
"""
