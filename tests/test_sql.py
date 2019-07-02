
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_cluster_solution.py

from cluster.api.sql import database_query as query
from tests.add_data import add_entries
from cluster.database.data_models import Dataset

def test_dataset_two(session, app):

    add_entries(session)
    #x

    result = query(
        'SELECT * FROM dataset'
    )
    assert result == \
'''id	name	uuid	species	organ	cell_count	disease	platform	description	data_source_url	publication_url
1	dataset1	uuid1	dog	organ1	1	disease1	platform1	description1	data_source_url1	publication_url1
2	dataset2	uuid2	cat	organ2	2	disease2	platform2	description2	data_source_url2	publication_url2'''



def test_cluster_solution(session):

    add_entries(session)

    result = query(
        'SELECT * FROM cluster_solution'
    )

    assert True

    assert result == \
'''id	name	description	method	method_implementation	method_url	method_parameters	scores	analyst\tlikes\texpression_hash	dataset_id
1	cluster_solution1	description1	method1	method_implementation1	method_url1	method_parameters1	scores1	analyst1\t1\texpression_hash1	1'''


def test_cluster(session):

    add_entries(session)
    result = query(
        'SELECT * FROM cluster'
    )

    assert result == \
'''id	name	label	description\tcell_count\tcluster_solution_id
1	cluster1	label1	description1\t1\t1
2	cluster2	label2	description2\t1\t1'''


def test_cell_of_cluster(session):
    add_entries(session)
    result = query(
            'SELECT * FROM cell_of_cluster'
    )

    assert result == \
'''id	name	cluster_id
1	sample1	1
2	sample2	2'''

def test_update(session):
    add_entries(session)
    result = query(
        'UPDATE dataset SET species = "kangaroo"' + \
         ' WHERE name = "dataset2"'
    )
    assert result == \
        '400 Updates to the database are not allowed, only read queries.'

def test_api(client, session):
    add_entries(session)
    response = client.get('/sql/select%20*%20from%20dataset')
    #print('response.decode:', response.data.decode("utf-8"))

    assert "text/plain" in response.content_type
    assert response.data.decode("utf-8") == \
'''id	name	uuid	species	organ	cell_count	disease	platform	description	data_source_url	publication_url
1	dataset1	uuid1	dog	organ1	1	disease1	platform1	description1	data_source_url1	publication_url1
2	dataset2	uuid2	cat	organ2	2	disease2	platform2	description2	data_source_url2	publication_url2'''

