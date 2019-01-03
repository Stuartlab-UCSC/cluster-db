
import pytest
from cluster.database.dataset_table import dataset
accept_tsv = 'text/tsv'
accept_json = 'json/application'
add_one_data = {
    "name": "dataset1",
    "species": "dog",
    "organ": None,
    "sampleCount": None,
    "abnormality": None,
    "primaryData": None,
    "scanpyObjectOfPrimaryData": None,
    "sampleMetadata": None,
    "primaryDataNormalizationStatus": None,
    "clusteringScript": None,
    "reasonableForTrajectoryAnalysis": None,
    "trajectoryAnalysisScript": None,
    "platform": None,
    "expressionDataSource": None,
    "expressionDataSourceURL": None
}
add_second_data = {
    "name": "dataset2",
    "species": "cat",
    "organ": None,
    "sampleCount": None,
    "abnormality": None,
    "primaryData": None,
    "scanpyObjectOfPrimaryData": None,
    "sampleMetadata": None,
    "primaryDataNormalizationStatus": None,
    "clusteringScript": None,
    "reasonableForTrajectoryAnalysis": None,
    "trajectoryAnalysisScript": None,
    "platform": None,
    "expressionDataSource": None,
    "expressionDataSourceURL": None
}

def lists_equal(l1, l2):
    return ((l1 > l2) - (l1 < l2)) == 0

def dicts_equal(d1, d2):
    # one way to compare since we're not using all keys yet:
    equal = True
    for key in d1.keys():
        if d2[key] != d2[key]:
            equal = False
            break
    return equal
    # TODO test all fields after dataset fields are firmed up.
    # TODO is there a better way to compare two dicts?
    #return lists_equal(d1.keys(), d2.keys()) && \
    #    lists_equal(d1.values(), d2.values())

def test_add_many_tsv(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset.tsv')
        assert result == None
        result = dataset.get_all(accept_json)
        assert dicts_equal(result[0], add_one_data)
        assert dicts_equal(result[1], add_second_data)


def test_add_many_tsv_bad_header(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_bad_header.tsv')
        assert result['status_code'] == 400
        assert result['message'] == 'Bad TSV header:\n' + \
                                    'expected: "name species"\n' + \
                                    '   given: "bad header"'


def test_add_many_tsv_too_many_columns(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_too_many_columns.tsv')
        assert result == None
        result = dataset.get_all(accept_json)
        assert dicts_equal(result[0], add_one_data)
        assert dicts_equal(result[1], add_second_data)


def test_add_many_tsv_not_enough_columns(app):
    with app.app_context():
        result = dataset.add_many_tsv('dataset_not_enough_columns.tsv')
        assert result['status_code'] == 400
        assert result['message'] == \
            'Database NOT NULL constraint failed: dataset.species'


def test_add_one(app):
    with app.app_context():
        result = dataset.add_one(add_one_data)
        assert result == None
        result = dataset.get_one('dataset1', accept_json)
        assert dicts_equal(result, add_one_data)


def test_add_duplicate(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.add_one(add_one_data)
        assert result['status_code'] == 400
        assert result['message'] == \
            'Database UNIQUE constraint failed: dataset.name'


def test_delete(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.delete('dataset1')
        assert result == None
        result = dataset.get_one('dataset1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset1'


def test_delete_not_found(app):
    with app.app_context():
        result = dataset.delete('dataset1')
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset1'


def test_delete_with_children(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.delete_with_children('dataset1')
        assert result == None
        result = dataset.get_one('dataset1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset1'

# TODO test delete of all children

def test_delete_with_children_this_not_found(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.delete_with_children('dataset666')
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset666'


def test_get_all_of_one(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.get_all(accept_json)
        assert len(result) == 1
        assert dicts_equal(result[0], add_one_data)


def test_get_all_of_one_as_tsv(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.get_all(accept_tsv)
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_all_of_two(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        dataset.add_one(add_second_data)
        result = dataset.get_all(accept_json)
        assert len(result) == 2
        assert dicts_equal(result[0], add_one_data)
        assert dicts_equal(result[1], add_second_data)


def test_get_all_of_two_as_tsv(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        dataset.add_one(add_second_data)
        result = dataset.get_all(accept_tsv)
        assert len(result) == 38
        assert result == 'name\tspecies\ndataset1\tdog\ndataset2\tcat'
        # TODO test all fields after dataset fields are firmed up.


def test_get_all_with_none(app):
    with app.app_context():
        result = dataset.get_all(accept_json)
        assert len(result) == 0


def test_get_by_parent(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.get_by_parent('noParentTable', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'There is no parent table for datasets'


def test_get_by_parent_child_not_found(app):
    # With no parent table, this will never happen.
    pass


def test_get_by_parent_parent_not_found(app):
    # With no parent table, this will never happen.
    pass


def test_get_one(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.get_one('dataset1', accept_json)
        assert result['name'] == 'dataset1'


def test_get_one_as_tsv(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.get_one('dataset1', accept_tsv)
        assert len(result) == 25
        assert result == 'name\tspecies\ndataset1\tdog'
        # TODO test all fields after dataset fields are firmed up.


def test_get_one_not_found(app):
    with app.app_context():
        result = dataset.get_one('dataset1', accept_json)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset1'


def test_update(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.update('dataset1', 'species', 'newt')
        assert result == None
        result = dataset.get_one('dataset1', accept_json)
        assert result['species'] == 'newt'


def test_update_not_found(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.update('dataset666', '_id', 666)
        assert result['status_code'] == 404
        assert result['message'] == 'Not found: dataset: dataset666'


def test_update_id(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.update('dataset1', '_id', 666)
        assert result['status_code'] == 400
        assert result['message'] == "Database invalid field: _id"


def test_update_bad_field(app):
    with app.app_context():
        dataset.add_one(add_one_data)
        result = dataset.update('dataset1', 'junkField', 666)
        assert result['status_code'] == 400
        assert result['message'] == "Database invalid field: junkField"

