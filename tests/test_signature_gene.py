
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts

one_data_got = merge_dicts(ad.add_one_signature_gene, {})
del(one_data_got['signature_gene_set'])
one_data_added = merge_dicts(ad.add_one_signature_gene, {'signature_gene_set_id': 1})
del(one_data_added['signature_gene_set'])

second_data_got = merge_dicts(ad.add_second_signature_gene, {})
del(second_data_got['signature_gene_set'])
second_data_added = merge_dicts(ad.add_second_signature_gene, {'signature_gene_set_id': 1})
del(second_data_added['signature_gene_set'])

def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    signature_gene_set.add_one(ad.add_one_signature_gene_set)

def test_add_one(app):
    with app.app_context():
        add_parents()
        result = signature_gene.add_one(ad.add_one_signature_gene)
        assert result == None
        result = signature_gene.get_one(
            'signature_gene1', ad.accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = signature_gene.add_one(ad.add_one_signature_gene)
        assert result == \
            '404 Parent not found: signature_gene_set: signature_gene_set1'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene.get_by_parent('signature_gene_set1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene.get_by_parent('signature_gene_setX', ad.accept_json)
        assert result == \
            '404 Parent not found: signature_gene_set: signature_gene_setX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene.get_one('signature_gene1', ad.accept_json)
        assert dicts_equal(result, one_data_added)
