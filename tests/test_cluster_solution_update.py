
# We don't duplicate tests aready done for common code in test_dataset.py.

import pytest, json
import tests.access_db_data as ad
from cluster.database_update.dataset_table import dataset
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.gene_set_table import gene_set
from cluster.database_update.cluster_table import cluster
from cluster.database.db_old import dicts_equal, merge_dicts


def add_parent():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)


def test_add_three_and_get_by_parent(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.add_one(
            ad.add_one_cluster_solution)
        assert result == 1
        result = cluster_solution.add_one(
            ad.add_second_cluster_solution)
        assert result == 2
        result = cluster_solution.add_one(
            ad.add_third_cluster_solution)
        assert result == 3

        #result = cluster_solution.get_all()
        #print('result:', result)
        #assert false

        # verify first two adds.
        result = cluster_solution.get_by_parent(['dataset1'])
        #print('result:', result)
        assert result == \
'''name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash
cluster_solution1	description1	method1	method_implementation1	method_url1	method_parameters1	scores1	analyst1	1	1	expression_hash1
cluster_solution2	description2	method2	method_implementation2	method_url2	method_parameters2	scores2	analyst2	0	2	expression_hash2'''

        # verify last add
        result = cluster_solution.get_by_parent(['dataset2'])
        #print('result:', result)
        assert result == \
'''name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash
cluster_solution2	description3	method3	method_implementation3	method_url3	method_parameters3	scores3	analyst3	1	3	expression_hash3'''

        # delete one
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == None
        
        # verify delete
        result = cluster_solution.get_all()
        print('result:', result)
        assert result == \
'''name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash	dataset_id
cluster_solution2	description2	method2	method_implementation2	method_url2	method_parameters2	scores2	analyst2	0	2	expression_hash2	1
cluster_solution2	description3	method3	method_implementation3	method_url3	method_parameters3	scores3	analyst3	1	3	expression_hash3	2'''


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = cluster_solution.add_one(
            ad.add_one_cluster_solution)
        assert result == '404 Not found: parent'


def test_delete_not_found(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == '404 Not found: cluster_solution: cluster_solution1'


def test_delete_has_children_gene_set(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        gene_set.add_tsv('gene_set.tsv',
            ['cluster_solution1', 'dataset1'])
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_delete_has_children_cluster(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        cluster.add_tsv('cluster.tsv', ['cluster_solution1', 'dataset1'])
        result = cluster_solution.delete_one(
            'cluster_solution1', ['dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_get_by_parent_child_not_found(app):
    with app.app_context():
        add_parent()
        result = cluster_solution.get_by_parent(['dataset1'])
        assert result == \
            '404 Not found: cluster_solution with dataset: dataset1'


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parent()
        cluster_solution.add_one(ad.add_one_cluster_solution)
        result = cluster_solution.get_by_parent(['datasetX'])
        assert result == '404 Not found: parent'


def test_api_add_one_and_get_by_parent(app, client):
    # add one
    with app.app_context():
        add_parent()
        response = ad.post_json(
            client, '/cluster-solution-update/add', ad.add_one_cluster_solution)
        response = ad.post_json(
            client, '/cluster-solution-update/add', ad.add_third_cluster_solution)
        #print('response.decode', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain

        # get by parent
        response = client.get(
            '/cluster-solution-update/get_by/dataset/dataset1')
        assert response.content_type == ad.text_plain
        #print('response.data:', response.data)
        #print('response.decode', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == \
'''name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash
cluster_solution1	description1	method1	method_implementation1	method_url1	method_parameters1	scores1	analyst1	1	1	expression_hash1'''

        # delete
        response = client.get(
            '/cluster-solution-update' +
            '/delete/cluster_solution1' +
            '/dataset/dataset1')
        #print('response.data:', response.data)
        #print('response.decode', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain

        # verify delete
        response = client.get(
            '/cluster-solution-update/get_by/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
        	'404 Not found: cluster_solution with dataset: dataset1'
        
        # verify delete did not delete another
        response = client.get(
            '/cluster-solution-update/get_by/dataset/dataset2')
        assert response.content_type == ad.text_plain
        print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == \
'''name	description	method	method_implementation	method_url	method_parameters	scores	analyst	analyst_favorite	likes	expression_hash
cluster_solution2	description3	method3	method_implementation3	method_url3	method_parameters3	scores3	analyst3	1	3	expression_hash3'''

