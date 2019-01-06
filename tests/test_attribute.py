
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.cluster_table import cluster
from cluster.database.attribute_table import attribute
from cluster.database.db import dicts_equal, merge_dicts

one_data_got = merge_dicts(ad.add_one_attribute, {})
del(one_data_got['cluster'])
one_data_added = merge_dicts(ad.add_one_attribute, {'cluster_id': 1})
del(one_data_added['cluster'])

# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    cluster.add_one(ad.add_one_cluster)

def test_add_one(app):
    with app.app_context():
        add_parents()
        result = attribute.add_one(ad.add_one_attribute)
        assert result == None
        result = attribute.get_one(
            'attribute1', ad.accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = attribute.add_one(ad.add_one_attribute)
        assert result == '404 Parent not found: cluster: cluster1'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        attribute.add_one(ad.add_one_attribute)
        result = attribute.get_by_parent('cluster1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        attribute.add_one(ad.add_one_attribute)
        result = attribute.get_by_parent('clusterX', ad.accept_json)
        assert result== '404 Parent not found: cluster: clusterX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        attribute.add_one(ad.add_one_attribute)
        result = attribute.get_one('attribute1', ad.accept_json)
        assert dicts_equal(result, one_data_added)
