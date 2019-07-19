


from cluster.database.user_models import  UserExpression, ClusterGeneTable, ExpDimReduct, ExpCluster, CellTypeWorksheet, WorksheetUser

# These are all the global variables that will need access functions once the data serves more than worksheet.
TEST_STATE_PATH = "../users/test/test_state.json.gzip"
TEST_CLUSTER_TABLE_PATH = "../users/test/clusters_table.tab"
TEST_MARKERS_DICT_PATH = "../users/test/krigstien6000k_markers.json.gzip"
TEST_EXPRESSION_PICKLE_PATH = "../users/test/exp.pi"
TEST_CLUSTER_ID_PATH = "../users/test/louvain:res:1.50.pi"
TEST_XY_PATH = "../users/test/X_umap.pi"
DEFAULT_CLUSTER_SOLUTION="1"
DEFAULT_SCATTER_TYPE="umap"
# The cluster solution name matches what is int the cluster-id file and a key inside the markers.json.gzip
CLUSTER_SOLUTION_NAME = "louvain:res:1.50"

#You were getting the paths into the user directory correct...
# entries are defined as a tuple of dictionaries mapping to keys and the db.Model class
entries = []


worksheet = {
    "name": "test",
    "place": TEST_STATE_PATH
}

entries.append(
    (CellTypeWorksheet, worksheet)
)

worksheet_user = {
    "user_id": 1,
    "worksheet_id": 1
}

entries.append(
    (WorksheetUser, worksheet_user)
)

expression = {
    "id": 1,
    "species": "test",
    "organ": "test",
    "name": "test",
    "place": TEST_EXPRESSION_PICKLE_PATH,
    "worksheet_id": 1
}

entries.append(
    (UserExpression, expression)
)

dimreduct = {
    "name": "test",
    "expression_id": 1,
    "place": TEST_XY_PATH
}

entries.append(
    (ExpDimReduct, dimreduct)
)

cluster = {
    "id": 1,
    "name": "test",
    "expression_id": 1,
    "place": TEST_CLUSTER_TABLE_PATH
}

entries.append(
    (ExpCluster, cluster)
)

gene_table = {
    "place": TEST_MARKERS_DICT_PATH,
    "cluster_id": 1
}

entries.append(
    (ClusterGeneTable, gene_table)
)