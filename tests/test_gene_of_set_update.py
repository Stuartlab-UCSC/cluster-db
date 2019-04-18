
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database_update.dataset_table import dataset
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.gene_set_table import gene_set
from cluster.database_update.gene_of_set_table import gene_of_set
from cluster.database.db_old import dicts_equal, merge_dicts


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster_solution.add_one(ad.add_second_cluster_solution)
    gene_set.add_one(ad.add_one_gene_set, ['dataset1'])
    gene_set.add_one(ad.add_second_gene_set, ['dataset1'])
    gene_set.add_one(ad.add_third_gene_set, ['dataset1'])


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()

        # Add three sets of signature genes.
        result = gene_of_set.add_tsv('gene_of_set.tsv',
            ['gene_set1', 'cluster_solution1', 'dataset1'])
        assert result == 2
        result = gene_of_set.add_tsv('gene_of_set.tsv',
            ['gene_set2', 'cluster_solution1', 'dataset1'])
        assert result == 4
        result = gene_of_set.add_tsv('gene_of_set.tsv',
            ['gene_set2', 'cluster_solution2', 'dataset1'])
        assert result == 6

        # verify adds with get all
        result = gene_of_set.get_all()
        #print('result:', result)
        assert result ==  \
'''name	gene_set_id
gene_of_set1	1
gene_of_set2	1
gene_of_set1	2
gene_of_set2	2
gene_of_set1	3
gene_of_set2	3'''

        # get by parent
        result = gene_of_set.get_by_parent(
            ['gene_set1', 'cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  \
'''name
gene_of_set1
gene_of_set2'''

        # delete
        result = gene_of_set.delete_by_parent(
            ['gene_set2', 'cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  None
        
        # verify delete with get all
        result = gene_of_set.get_all()
        #print('result:', result)
        assert result ==  \
'''name	gene_set_id
gene_of_set1	1
gene_of_set2	1
gene_of_set1	3
gene_of_set2	3'''


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        gene_of_set.add_tsv('gene_of_set.tsv',
            ['gene_set1', 'cluster_solution1', 'dataset1'])
        result = gene_of_set.get_by_parent(['gene_setX',
            'cluster_solution1', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(client, app):
    # add many tsv
    with app.app_context():
        add_parents()
        
        # Add three sets of signature genes.
        response = client.get(
            '/gene-of-set-update/add' + \
            '/tsv_file/gene_of_set.tsv' + \
            '/gene_set/gene_set1' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'
        response = client.get(
            '/gene-of-set-update/add' + \
            '/tsv_file/gene_of_set.tsv' + \
            '/gene_set/gene_set2' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/gene-of-set-update/add' + \
            '/tsv_file/gene_of_set.tsv' + \
            '/gene_set/gene_set2' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '6'

        # verify adds with get all
        response = client.get('/gene-of-set-update')
        #print('response.decode:', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") ==  \
'''name	gene_set_id
gene_of_set1	1
gene_of_set2	1
gene_of_set1	2
gene_of_set2	2
gene_of_set1	3
gene_of_set2	3'''

        # get by parent
        response = client.get(
            '/gene-of-set-update/get_by' + \
            '/gene_set/gene_set1' + \
            'cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        #print('response.data:', response.data)
        assert response.data.decode("utf-8") == \
'''name
gene_of_set1
gene_of_set2'''

        # delete
        response = client.get(
            '/gene-of-set-update' + \
            '/delete_by' + \
            '/gene_set/gene_set2' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        #print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == 'None'
        
        # verify the delete with a get all
        response = client.get('/gene-of-set-update')
        print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") ==  \
'''name	gene_set_id
gene_of_set1	1
gene_of_set2	1
gene_of_set1	3
gene_of_set2	3'''
