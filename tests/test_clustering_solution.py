
# We don't duplicate tests aready done for common code in test_dataset.py.

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.db import dicts_equal, merge_dicts

one_data_got = merge_dicts(ad.add_one_clustering_solution, {})
del(one_data_got['dataset'])
one_data_added = merge_dicts(ad.add_one_clustering_solution, {'dataset_id': 1})
del(one_data_added['dataset'])

second_data_got = merge_dicts(ad.add_second_clustering_solution, {})
del(second_data_got['dataset'])
second_data_added = merge_dicts(ad.add_second_clustering_solution, {'dataset_id': 1})
del(second_data_added['dataset'])


def test_add_many_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'dataset1')
        assert result == None
        result = clustering_solution.get_all(ad.accept_json)
        assert dicts_equal(result[0], one_data_added)
        assert dicts_equal(result[1], second_data_added)


def test_add_many_tsv_no_parent_supplied(app):
    with app.app_context():
        result = clustering_solution.add_many_tsv('clustering_solution.tsv')
        assert result['status_code'] == 400
        assert result['message'] == 'Parent was not supplied: dataset'


def test_add_many_tsv_parent_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_many_tsv(
            'clustering_solution.tsv', 'datasetX')
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: datasetX'


def test_add_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.add_one(ad.add_one_clustering_solution)
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', ad.accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = clustering_solution.add_one(ad.add_one_clustering_solution)
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: dataset1'


def test_delete(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.delete('clustering_solution1')
        assert result == None
        result = clustering_solution.get_one(
            'clustering_solution1', ad.accept_json)
        assert result['status_code'] == 404
        assert result['message'] == \
            'Not found: clustering_solution: clustering_solution1'


def test_delete_has_children(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = clustering_solution.delete('clustering_solution1')
        assert result['status_code'] == 400
        assert result['message'] == \
            'There are children that would be orphaned, delete them first'


def test_delete_including_children_with_no_children(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.delete_including_children('clustering_solution1')
        assert result == None
        result = clustering_solution.get_one('clustering_solution1', ad.accept_json)
        assert result['status_code'] == 404
        assert result['message'] == \
            'Not found: clustering_solution: clustering_solution1'


def test_delete_including_children_this_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.delete_including_children('clustering_solution1')
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: clustering_solution: clustering_solution1'


def test_get_by_parent_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_one_tsv(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_tsv)
        assert len(result) == 194
        assert result == \
            'name\tmethod\tmethod_implementation\tmethod_url\tmethod_parameters\tanalyst\tsecondary\tdataset_id\nclustering_solution1\tmethod1\tmethod_implementation1\tmethod_url1\tmethod_parameters1\tanalyst1\tsecondary1'


def test_get_by_parent_two(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        clustering_solution.add_one(ad.add_second_clustering_solution)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert len(result) == 2
        assert dicts_equal(result[0], one_data_got)
        assert dicts_equal(result[1], second_data_got)


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        result = clustering_solution.get_by_parent('dataset1', ad.accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_by_parent('datasetX', ad.accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Parent not found: dataset: datasetX'


def test_get_one(app):
    with app.app_context():
        dataset.add_one(ad.add_one_dataset)
        clustering_solution.add_one(ad.add_one_clustering_solution)
        result = clustering_solution.get_one('clustering_solution1', ad.accept_json)
        assert dicts_equal(result, one_data_added)
