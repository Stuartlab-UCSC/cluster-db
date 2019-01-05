
# We don't duplicate tests aready done for common code in test_dataset.py.

import pytest
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.dataset_table import dataset
accept_tsv = 'text/tsv'
accept_json = 'json/application'
add_one_data = {
    "name": "clustering_solution1",
    "method": "method1",
    "method_implementation": "method_implementation1",
    "method_url": "method_url1",
    "method_parameters": "method_parameters1",
    "analyst": "analyst1",
    "secondary": "secondary1",
    "dataset": "dataset1",
}
add_second_data = {
    "name": "clustering_solution2",
    "method": "method2",
    "method_implementation": "method_implementation2",
    "method_url": "method_url2",
    "method_parameters": "method_parameters2",
    "analyst": "analyst2",
    "secondary": "secondary2",
    "dataset": "dataset1",
}
add_one_dataset = {
    "name": "dataset1",
    "species": "dog"
}
def _merge_dicts(d1, d2):
    return {**d1, **d2}

one_data_got = _merge_dicts(add_one_data, {})
del(one_data_got['dataset'])
one_data_added = _merge_dicts(add_one_data, {'dataset_id': 1})
del(one_data_added['dataset'])

second_data_got = _merge_dicts(add_second_data, {})
del(second_data_got['dataset'])
second_data_added = _merge_dicts(add_second_data, {'dataset_id': 1})
del(second_data_added['dataset'])

def lists_equal(l1, l2):
    return ((l1 > l2) - (l1 < l2)) == 0

def dicts_equal(d1, d2):
    # TODO is there a better way to compare two dicts?
    print('d1:', d1)
    print('d2:', d2)
    return lists_equal(list(d1.keys()), list(d2.keys())) and \
        lists_equal(list(d1.values()), list(d2.values()))


def test_add_many_tsv(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'dataset1')
        assert result == None
        result = clustering_solution.get_all(accept_json)
        assert dicts_equal(result[0], one_data_added)
        assert dicts_equal(result[1], second_data_added)


def test_add_many_tsv_no_parent_supplied(app):
    with app.app_context():
        result = clustering_solution.add_many_tsv('clustering_solution.tsv')
        assert result['status_code'] == 400
        assert result['message'] == 'Parent was not supplied: dataset'


def test_add_many_tsv_parent_not_found(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'datasetX')
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: datasetX'


def test_add_one(app):
    with app.app_context():
        print('test_add_one_parent_not_found:add_one_data:', add_one_data)
        dataset.add_one(add_one_dataset)
        result = clustering_solution.add_one(add_one_data)
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        #print('test_add_one_parent_not_found:add_one_data:', add_one_data)
        result = clustering_solution.add_one(add_one_data)
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: dataset1'

"""
def test_delete_including_children_no_children(app):
    with app.app_context():
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.delete_including_children('clustering_solution1')
        assert result == None
        result = clustering_solution.get_one('clustering_solution1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: clustering_solution: clustering_solution1'

def test_delete_including_children_with_children(app):
    with app.app_context():
        pass

def test_delete_including_children_this_not_found(app):
    with app.app_context():
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.delete_including_children('clustering_solution666')
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: clustering_solution: clustering_solution666'
"""

def test_get_by_parent_one(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.get_by_parent('dataset1', accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_one_tsv(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.get_by_parent('dataset1', accept_tsv)
        assert len(result) == 194
        assert result == \
            'name\tmethod\tmethod_implementation\tmethod_url\tmethod_parameters\tanalyst\tsecondary\tdataset_id\nclustering_solution1\tmethod1\tmethod_implementation1\tmethod_url1\tmethod_parameters1\tanalyst1\tsecondary1'


def test_get_by_parent_two(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        clustering_solution.add_one(add_one_data)
        clustering_solution.add_one(add_second_data)
        result = clustering_solution.get_by_parent('dataset1', accept_json)
        assert len(result) == 2
        assert dicts_equal(result[0], one_data_got)
        assert dicts_equal(result[1], second_data_got)


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        result = clustering_solution.get_by_parent('dataset1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.get_by_parent('dataset1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: dataset1'


def test_get_one(app):
    with app.app_context():
        dataset.add_one(add_one_dataset)
        clustering_solution.add_one(add_one_data)
        result = clustering_solution.get_one('clustering_solution1', accept_json)
        assert dicts_equal(result, one_data_added)
