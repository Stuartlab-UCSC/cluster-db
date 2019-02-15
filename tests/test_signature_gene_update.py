
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database_update.dataset_table import dataset
from cluster.database_update.cluster_solution_table import cluster_solution
from cluster.database_update.signature_gene_set_table import signature_gene_set
from cluster.database_update.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster_solution.add_one(ad.add_second_cluster_solution)
    signature_gene_set.add_one(ad.add_one_signature_gene_set, ['dataset1'])
    signature_gene_set.add_one(ad.add_second_signature_gene_set, ['dataset1'])
    signature_gene_set.add_one(ad.add_third_signature_gene_set, ['dataset1'])


def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()

        # Add three sets of signature genes.
        result = signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set1', 'cluster_solution1', 'dataset1'])
        assert result == 2
        result = signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set2', 'cluster_solution1', 'dataset1'])
        assert result == 4
        result = signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set2', 'cluster_solution2', 'dataset1'])
        assert result == 6

        # verify adds with get all
        result = signature_gene.get_all()
        #print('result:', result)
        assert result ==  \
'''name	signature_gene_set_id
signature_gene1	1
signature_gene2	1
signature_gene1	2
signature_gene2	2
signature_gene1	3
signature_gene2	3'''

        # get by parent
        result = signature_gene.get_by_parent(
            ['signature_gene_set1', 'cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  \
'''name
signature_gene1
signature_gene2'''

        # delete
        result = signature_gene.delete_by_parent(
            ['signature_gene_set2', 'cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  None
        
        # verify delete with get all
        result = signature_gene.get_all()
        #print('result:', result)
        assert result ==  \
'''name	signature_gene_set_id
signature_gene1	1
signature_gene2	1
signature_gene1	3
signature_gene2	3'''


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set1', 'cluster_solution1', 'dataset1'])
        result = signature_gene.get_by_parent(['signature_gene_setX',
            'cluster_solution1', 'dataset1'])
        assert result == \
            '404 Not found: parent'


def test_api(client, app):
    # add many tsv
    with app.app_context():
        add_parents()
        
        # Add three sets of signature genes.
        response = client.get(
            '/signature_gene_update/add' + \
            '/tsv_file/signature_gene.tsv' + \
            '/signature_gene_set/signature_gene_set1' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'
        response = client.get(
            '/signature_gene_update/add' + \
            '/tsv_file/signature_gene.tsv' + \
            '/signature_gene_set/signature_gene_set2' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '4'
        response = client.get(
            '/signature_gene_update/add' + \
            '/tsv_file/signature_gene.tsv' + \
            '/signature_gene_set/signature_gene_set2' + \
            '/cluster_solution/cluster_solution2' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '6'

        # verify adds with get all
        response = client.get('/signature_gene update')
        #print('response.decode:', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") ==  \
'''name	signature_gene_set_id
signature_gene1	1
signature_gene2	1
signature_gene1	2
signature_gene2	2
signature_gene1	3
signature_gene2	3'''

        # get by parent
        response = client.get(
            '/signature_gene_update/get_by' + \
            '/signature_gene_set/signature_gene_set1' + \
            'cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        #print('response.data:', response.data)
        assert response.data.decode("utf-8") == \
'''name
signature_gene1
signature_gene2'''

        # delete
        response = client.get(
            '/signature_gene update' + \
            '/delete_by' + \
            '/signature_gene_set/signature_gene_set2' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        #print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == 'None'
        
        # verify the delete with a get all
        response = client.get('/signature_gene update')
        print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") ==  \
'''name	signature_gene_set_id
signature_gene1	1
signature_gene2	1
signature_gene1	3
signature_gene2	3'''
