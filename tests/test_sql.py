
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database_update.cluster_attribute_table import cluster_attribute
from cluster.database_update.cell_of_cluster_table import cell_of_cluster
from cluster.database_update.cluster_table import cluster
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.dataset_table import dataset
from cluster.database.db import dicts_equal, merge_dicts
from cluster.database.query import query
from cluster.database_update.gene_set_table import gene_set
from cluster.database_update.gene_of_set_table import gene_of_set


def add_data():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster.add_tsv('cluster.tsv', ['cluster_solution1', 'dataset1'])
    cell_of_cluster.add_tsv('cell_of_cluster.tsv',
        ['cluster_solution1', 'dataset1'])
    cluster_attribute.add_tsv('cluster_attribute.tsv', ['cluster_solution1', 'dataset1'])
    gene_set.add_tsv(
            'gene_set.tsv', ['cluster_solution1', 'dataset1'])
    gene_of_set.add_tsv('gene_of_set.tsv',
                ['gene_set1', 'cluster_solution1', 'dataset1'])

def test_dataset_two(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM dataset'
        )
        print('result', result)
        assert result == \
'''id	name	uuid	species	organ	cell_count	disease	platform	description	data_source_url	publication_url
1	dataset1	uuid1	dog	organ1	1	disease1	platform1	description1	data_source_url1	publication_url1
2	dataset2	uuid2	cat	organ2	2	disease2	platform2	description2	data_source_url2	publication_url2'''


def test_cluster_solution(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cluster_solution'
        )
        print('result', result)
        assert result == \
'''id	name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash	dataset_id
1	cluster_solution1	description1	method1	method_implementation1	method_url1	method_parameters1	scores1	analyst1	1	1	expression_hash1	1'''


def test_cluster(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cluster'
        )
        print('result', result)
        assert result == \
'''id	name	label	description	cluster_solution_id
1	cluster1	label1	description1	1
2	cluster2	label2	description2	1'''


def test_cluster_attribute(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cluster_attribute'
        )
        print('result', result)
        assert result == \
'''id	name	value	cluster_id
1	cluster_attribute1	value11	1
2	cluster_attribute2	value21	1
3	cluster_attribute1	value12	2
4	cluster_attribute2	value22	2'''


def test_cell_of_cluster(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM cell_of_cluster'
        )
        print('result', result)
        assert result == \
'''id	name	cluster_id
1	sample1	1
2	sample2	2
3	sample3	1
4	sample4	2'''


def test_gene_of_set(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM gene_of_set'
        )
        print('result', result)
        assert result == \
'''id	name	gene_set_id
1	gene_of_set1	1
2	gene_of_set2	1'''


def test_gene_set(app):
    with app.app_context():
        add_data()
        result = query(
            'SELECT * FROM gene_set'
        )
        print('result', result)
        assert result == \
'''id	name	type	method	cluster_solution_id
1	gene_set1	signature	method1	1
2	gene_set2	signature	method2	1'''


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
'''id	name	uuid	species	organ	cell_count	disease	platform	description	data_source_url	publication_url
1	dataset1	uuid1	dog	organ1	1	disease1	platform1	description1	data_source_url1	publication_url1
2	dataset2	uuid2	cat	organ2	2	disease2	platform2	description2	data_source_url2	publication_url2'''
