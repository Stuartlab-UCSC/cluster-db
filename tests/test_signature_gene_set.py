
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


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)


def add_parents_tsv(client):
    client.post('/api/dataset/add',
        data=json.dumps(ad.add_one_dataset), headers=ad.json_headers)
    client.post('/api/clustering_solution/add',
        data=json.dumps(ad.add_one_clustering_solution),
        headers=ad.json_headers)


def test_add_one(app):
    with app.app_context():
        add_parents()
        result = signature_gene_set.add_one(ad.add_one_signature_gene_set)
        assert result == None
        result = signature_gene_set.get_one(
            'signature_gene_set1', ad.accept_json)
        assert dicts_equal(result, ad.add_one_signature_gene_set)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = signature_gene_set.add_one(ad.add_one_signature_gene_set)
        assert result == \
            '404 Parent not found: clustering_solution: clustering_solution1'


def test_delete_has_children(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene_set.delete('signature_gene_set1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_by_parent(
            'clustering_solution1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got_by_parent)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_by_parent(
            'clustering_solutionX', ad.accept_json)
        assert result == \
            '404 Parent not found: clustering_solution: clustering_solutionX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_one('signature_gene_set1',
            ad.accept_json)
        assert dicts_equal(result, ad.add_one_signature_gene_set)


def test_json_api(client):
    # add one
    add_parents_tsv(client)
    response = client.post('/api/signature_gene_set/add',
        data=json.dumps(ad.add_one_signature_gene_set),
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert response.data == b'null\n'

    # get one
    response = client.get('/api/signature_gene_set/signature_gene_set1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json, ad.add_one_signature_gene_set)

    # get by parent
    response = client.get('/api/signature_gene_set/' + \
        'get_by_clustering_solution/clustering_solution1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], one_data_got_by_parent)

    # update
    response = client.get('/api/signature_gene_set/update/name/' + \
        'signature_gene_set1/field/name/value/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/signature_gene_set/signature_gene_set3',
        headers=ad.json_headers)
    print('response.json:', response.json)
    print('response.data:', response.data.decode("utf-8"))
    print('     expected:',one_data_got_by_parent)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json, one_data_updated)

    # delete
    response = client.get('/api/signature_gene_set/delete/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/signature_gene_set/signature_gene_set3')
    assert response.json == \
        '404 Not found: signature_gene_set: signature_gene_set3'


def test_tsv_api(client):
    # add many tsv
    add_parents_tsv(client)
    response = client.get('/api/signature_gene_set/add_many/tsv_file/' + \
        'signature_gene_set.tsv/clustering_solution/clustering_solution1')
    assert response.content_type == ad.accept_json
    assert response.data.decode("utf-8") == 'null\n'

    # get one
    response = client.get('/api/signature_gene_set/signature_gene_set1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	method	clustering_solution
signature_gene_set1	method1	clustering_solution1'''

    # get by parent
    response = client.get('/api/signature_gene_set/' + \
        'get_by_clustering_solution/clustering_solution1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''

    # update
    response = client.get('/api/signature_gene_set/update/name' + \
        '/signature_gene_set1/field/name/value/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/signature_gene_set/signature_gene_set3',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	method	clustering_solution
signature_gene_set3	method1	clustering_solution1'''

    # delete
    response = client.get(
        '/api/signature_gene_set/delete/signature_gene_set3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/signature_gene_set/signature_gene_set3',
        headers=ad.tsv_headers)
    assert response.data.decode("utf-8") == \
        '404 Not found: signature_gene_set: signature_gene_set3'


