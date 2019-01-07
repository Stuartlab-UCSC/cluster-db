
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
one_data_added = merge_dicts(ad.add_one_clustering_solution, {'dataset_id': 1})
del(one_data_added['dataset'])
one_data_updated = merge_dicts(ad.add_one_clustering_solution, {})
one_data_updated['name'] = 'clustering_solution3'

second_data_got_by_parent = merge_dicts(ad.add_second_clustering_solution, {})
second_data_got_all = merge_dicts(ad.add_second_clustering_solution, {})
del(second_data_got_by_parent['dataset'])


def test_add_many_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'dataset1')
        assert result == None
        result = clustering_solution.get_all(ad.accept_json)
        assert dicts_equal(result[0], ad.add_one_clustering_solution)
        assert dicts_equal(result[1], ad.add_second_clustering_solution)


def test_add_many_tsv_no_parent_supplied(app):
    with app.app_context():
        result = clustering_solution.add_many_tsv('clustering_solution.tsv')
        assert result == '400 Parent was not supplied: dataset'


def test_add_many_tsv_parent_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'datasetX')
        assert result== '404 Parent not found: dataset: datasetX'


def test_add_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_one(ad.add_one_clustering_solution)
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', ad.accept_json)
        assert dicts_equal(result, ad.add_one_clustering_solution)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = clustering_solution.add_one(ad.add_one_clustering_solution)
        assert result == '404 Parent not found: dataset: dataset1'


def test_delete(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.delete('clustering_solution1')
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', ad.accept_json)
        assert result == \
            '404 Not found: clustering_solution: clustering_solution1'


def test_delete_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.delete('clustering_solution1')
        assert result == \
            '404 Not found: clustering_solution: clustering_solution1'


def test_delete_has_children_signature_gene_set(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = clustering_solution.delete('clustering_solution1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_delete_has_children_cluster(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        cluster.add_one(ad.add_one_cluster)
        result = clustering_solution.delete('clustering_solution1')
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_get_all(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        clustering_solution.add_one(ad.add_second_clustering_solution)
        result = clustering_solution.get_all(ad.accept_json)
        assert dicts_equal(result[0], one_data_got_all)
        assert dicts_equal(result[1], second_data_got_all)


def test_get_all_tsv(app):
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        clustering_solution.add_one(ad.add_second_clustering_solution)
        result = clustering_solution.get_all(ad.accept_tsv)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary	dataset
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0	dataset1
clustering_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1	dataset1'''

def test_get_by_parent_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got_by_parent)


def test_get_by_parent_one_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_tsv)
        assert len(result) == 174
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0'''


def test_get_by_parent_two(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        clustering_solution.add_one(ad.add_second_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert len(result) == 2
        assert dicts_equal(result[0], one_data_got_by_parent)
        assert dicts_equal(result[1], second_data_got_by_parent)


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert result == '404 Not found: with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('datasetX', ad.accept_json)
        assert result == '404 Parent not found: dataset: datasetX'


def test_get_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_one('clustering_solution1',
            ad.accept_json)
        assert dicts_equal(result, ad.add_one_clustering_solution)


def test_get_one_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_one('clustering_solution1',
            ad.accept_tsv)
        assert result == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary	dataset
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0	dataset1'''


def test_json_api(client):
    # add one
    client.post('/api/dataset/add',
        data=json.dumps(ad.add_one_dataset), headers=ad.json_headers)
    response = client.post('/api/clustering_solution/add',
        data=json.dumps(ad.add_one_clustering_solution),
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert response.data == b'null\n'

    # get one
    response = client.get('/api/clustering_solution/clustering_solution1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json, ad.add_one_clustering_solution)

    # get by parent
    response = client.get('/api/clustering_solution/get_by_dataset/dataset1',
        headers=ad.json_headers)
    assert response.content_type == ad.accept_json
    assert dicts_equal(response.json[0], one_data_got_by_parent)

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


def test_tsv_api(client):
    # add many tsv
    client.post('/api/dataset/add',
        data=json.dumps(ad.add_one_dataset), headers=ad.json_headers)
    response = client.get('/api/clustering_solution/add_many/tsv_file/' + \
        'clustering_solution.tsv/dataset/dataset1')
    assert response.content_type == ad.accept_json
    assert response.data == b'null\n'

    # get one
    response = client.get('/api/clustering_solution/clustering_solution1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary	dataset
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0	dataset1'''

    # get by parent
    response = client.get('/api/clustering_solution/get_by_dataset/dataset1',
        headers=ad.tsv_headers)
    assert response.content_type == ad.accept_tsv
    assert response.data.decode("utf-8") == \
'''name	method	method_implementation	method_url	method_parameters	analyst	secondary
clustering_solution1	method1	method_implementation1	method_url1	method_parameters1	analyst1	0
clustering_solution2	method2	method_implementation2	method_url2	method_parameters2	analyst2	1'''

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


