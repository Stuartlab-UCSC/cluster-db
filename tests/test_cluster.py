
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.attribute_table import attribute
from cluster.database.cluster_assignment_table import cluster_assignment
from cluster.database.db import dicts_equal, merge_dicts

one_data_got = merge_dicts(ad.add_one_cluster, {})
del(one_data_got['clustering_solution'])
one_data_added = merge_dicts(ad.add_one_cluster, {'clustering_solution_id': 1})
del(one_data_added['clustering_solution'])


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)


def test_add_one(app):
    with app.app_context():
        add_parents()
        result = cluster.add_one(ad.add_one_cluster)
        assert result == None
        result = cluster.get_one('cluster1', ad.accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = cluster.add_one(ad.add_one_cluster)
        assert result == \
            '404 Parent not found: clustering_solution: clustering_solution1'


def test_delete_has_children_attribute(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        attribute.add_one(ad.add_one_attribute)
        result = cluster.delete('cluster1')
        assert result == \
            '400 There are children that would be orphaned, delete them first'


def test_delete_has_children_cluster_assignment(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        cluster_assignment.add_one(ad.add_one_cluster_assignment)
        result = cluster.delete('cluster1')
        assert result == \
            '400 There are children that would be orphaned, delete them first'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        result = cluster.get_by_parent('clustering_solution1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        result = cluster.get_by_parent('clustering_solutionX', ad.accept_json)
        assert result == '404 Parent not found: clustering_solution: clustering_solutionX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        cluster.add_one(ad.add_one_cluster)
        result = cluster.get_one('cluster1', ad.accept_json)
        assert dicts_equal(result, one_data_added)
