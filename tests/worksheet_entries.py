
import datetime
from cluster.database.user_models import User, UserExpression, ClusterGeneTable, ExpDimReduct, ExpCluster, CellTypeWorksheet, WorksheetUser
from flask import current_app
entries = []

user = {
    "email": "test@test.com",
    "password": current_app.user_manager.hash_password("testT1234"),
    "email_confirmed_at": datetime.datetime.utcnow(),

}


entries.append(
    (User, user)
)

worksheet = {
    "name": "test",
    "place": "state"
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
    "place": "expression",
    "worksheet_id":1
}

entries.append(
    (UserExpression, expression)
)

dimreduct = {
    "name": "test",
    "expression_id": 1,
    "place": "xys"
}

entries.append(
    (ExpDimReduct, dimreduct)
)

cluster = {
    "id": 1,
    "name": "test",
    "expression_id": 1,
    "place": "cluster_solution"
}

entries.append(
    (ExpCluster, cluster)
)

gene_table = {
    "place": "gene_table",
    "cluster_id": 1
}

entries.append(
    (ClusterGeneTable, gene_table)
)