

from cluster.api.user import TEST_STATE_PATH, TEST_MARKERS_DICT_PATH, TEST_CLUSTER_ID_PATH, TEST_XY_PATH, TEST_EXPRESSION_PICKLE_PATH, TEST_CLUSTER_TABLE_PATH
from cluster.database.user_models import  UserExpression, ClusterGeneTable, ExpDimReduct, ExpCluster, CellTypeWorksheet, WorksheetUser


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