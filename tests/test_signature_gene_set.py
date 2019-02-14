
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.cluster_solution_table import cluster_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    dataset.add_one(ad.add_second_dataset)
    cluster_solution.add_one(ad.add_one_cluster_solution)
    cluster_solution.add_one(ad.add_second_cluster_solution)
    cluster_solution.add_one(ad.add_third_cluster_solution)

def test_db(app):
    with app.app_context():
        add_parents()
        result = signature_gene_set.add_one(
            ad.add_one_signature_gene_set, ['dataset1'])
        result = signature_gene_set.add_one(
            ad.add_second_signature_gene_set, ['dataset1'])
        result = signature_gene_set.add_one(
            ad.add_third_signature_gene_set, ['dataset2'])
        assert result == 3
        
        # verify adds with get all
        result = signature_gene_set.get_all()
        #print('result:', result)
        assert result ==  \
'''name	method	cluster_solution_id
signature_gene_set1	method1	1
signature_gene_set2	method2	1
signature_gene_set2	method2	3'''

        # get by parent
        result = signature_gene_set.get_by_parent(
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''

        # delete one.
        result = signature_gene_set.delete_one('signature_gene_set1',
            ['cluster_solution1', 'dataset1'])
        assert result == None

        # verify it was deleted
        result = signature_gene_set.get_by_parent(
            ['cluster_solution1', 'dataset1'])
        #print('result:', result)
        assert result ==  \
'''name	method
signature_gene_set2	method2'''

        # verify the rest were left untouched.
        result = signature_gene_set.get_all()
        print('result:', result)
        assert result ==  \
'''name	method	cluster_solution_id
signature_gene_set2	method2	1
signature_gene_set2	method2	3'''


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_tsv(
            'signature_gene_set.tsv', ['cluster_solution1', 'dataset1'])
        result = signature_gene_set.get_by_parent(
            ['cluster_solutionX', 'dataset1'])
        assert result ==  '404 Not found: parent'


def test_delete_has_children(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set, ['dataset1'])
        signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set1', 'cluster_solution1', 'dataset1'])
        result = signature_gene_set.delete_one('signature_gene_set1',
            ['cluster_solution1', 'dataset1'])
        assert result == \
            '400 There are children that would be orphaned, delete those first'


def test_api(client, app):
    # add three
    with app.app_context():
        add_parents()
        response = ad.post_json(
            client,
            '/api/signature_gene_set/add' + \
            '/dataset/dataset1',
            ad.add_one_signature_gene_set)
        #print('response.data', response.data)
        assert response.content_type == ad.text_plain
        response = ad.post_json(
            client,
            '/api/signature_gene_set/add' + \
            '/dataset/dataset1',
            ad.add_second_signature_gene_set)
        #print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'
        response = ad.post_json(
            client,
            '/api/signature_gene_set/add' + \
            '/dataset/dataset2',
            ad.add_third_signature_gene_set)
        #print('response.data', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '3'

        # get all
        response = client.get('/api/signature_gene_set')
        print('response.data:', response.data.decode("utf-8"))
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	method	cluster_solution_id
signature_gene_set1	method1	1
signature_gene_set2	method2	1
signature_gene_set2	method2	3'''

        # get by parent
        response = client.get(
            '/api/signature_gene_set/get_by' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        #print('response.data:', response.data)
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == \
'''name	method
signature_gene_set1	method1
signature_gene_set2	method2'''

        # delete
        response = client.get(
            '/api/signature_gene_set' + \
            '/delete/signature_gene_set2' + \
            '/cluster_solution/cluster_solution1' + \
            '/dataset/dataset1')
        #print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == 'None'
        
        # check that it was really deleted
        response = client.get('/api/signature_gene_set')
        #print('response.data:', response.data.decode("utf-8"))
        assert response.data.decode("utf-8") == \
'''name	method	cluster_solution_id
signature_gene_set1	method1	1
signature_gene_set2	method2	3'''

