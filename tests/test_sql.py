
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database_update.attribute_table import attribute
from cluster.database_update.cell_assignment_table import cell_assignment
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.dataset_table import dataset
from cluster.database.db import dicts_equal, merge_dicts
from cluster.database.query import query
from cluster.database_update.signature_gene_set_table import signature_gene_set
from cluster.database_update.signature_gene_table import signature_gene


def add_data():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster.add_tsv('cluster.tsv', ['cluster_solution1', 'dataset1'])
    cell_assignment.add_tsv('cell_assignment.tsv',
        ['cluster_solution1', 'dataset1'])
    attribute.add_tsv('attribute.tsv', ['cluster_solution1', 'dataset1'])
    signature_gene_set.add_tsv(
            'signature_gene_set.tsv', ['cluster_solution1', 'dataset1'])
    signature_gene.add_tsv('signature_gene.tsv',
                ['signature_gene_set1', 'cluster_solution1', 'dataset1'])

def test_dataset_two(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM dataset'
        )
        print('result', result)
        assert result == \
'''id	name	species
1	dataset1	dog
2	dataset2	cat'''


def test_cluster_solution(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cluster_solution'
        )
        print('result', result)
        assert result == \
'''id	name	method	method_implementation	method_url	method_parameters	scores	analyst	secondary	dataset_id
1	cluster_solution1	method1	method_implementation1	method_url1	method_parameters1	scores1	analyst1	0	1'''


def test_cluster(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cluster'
        )
        print('result', result)
        assert result == \
'''id	name	cluster_solution_id
1	cluster1	1
2	cluster2	1'''


def test_attribute(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM attribute'
        )
        print('result', result)
        assert result == \
'''id	name	value	cluster_id
1	attribute1	value11	1
2	attribute2	value21	1
3	attribute1	value12	2
4	attribute2	value22	2'''


def test_cell_assignment(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cell_assignment'
        )
        print('result', result)
        assert result == \
'''id	name	cluster_id
1	sample1	1
2	sample2	2
3	sample3	1
4	sample4	2'''


def test_signature_gene(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM signature_gene'
        )
        print('result', result)
        assert result == \
'''id	name	signature_gene_set_id
1	signature_gene1	1
2	signature_gene2	1'''


def test_signature_gene_set(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM signature_gene_set'
        )
        print('result', result)
        assert result == \
'''id	name	method	cluster_solution_id
1	signature_gene_set1	method1	1
2	signature_gene_set2	method2	1'''


def test_update(app):
    with app.app_context():
        add_data()
        result = query(
            'UPDATE dataset SET species = "kangaroo"' + \
             ' WHERE name = "dataset2"'
        )
        assert result == \
            '400 Updates to the database are not allowed, only read queries.'

def test_api(client, app):
    with app.app_context():
        add_data()
        response = client.get('/sql/select%20*%20from%20dataset')
        print('response.decode:', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''id	name	species
1	dataset1	dog
2	dataset2	cat'''
