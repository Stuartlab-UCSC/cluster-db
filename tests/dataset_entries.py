
from cluster.database.data_models import Dataset, ClusterSolution, Cluster, CellAssignment

entries=[]

one_dataset = {
    "name": "dataset1",
    "uuid": "uuid1",
    "species": "dog",
    "organ": "organ1",
    "cell_count": 1,
    "disease": "disease1",
    "platform": "platform1",
    "description": "description1",
    "data_source_url": "data_source_url1",
    "publication_url": "publication_url1"
}

entries.append((Dataset, one_dataset))

second_dataset = {
    "name": "dataset2",
    "uuid": "uuid2",
    "species": "cat",
    "organ": "organ2",
    "cell_count": 2,
    "disease": "disease2",
    "platform": "platform2",
    "description": "description2",
    "data_source_url": "data_source_url2",
    "publication_url": "publication_url2"
}

entries.append(
    (Dataset, second_dataset)
)


one_cluster_solution = {
    "name": "cluster_solution1",
    "description": "description1",
    "method": "method1",
    "method_implementation": "method_implementation1",
    "method_url": "method_url1",
    "method_parameters": "method_parameters1",
    "scores": "scores1",
    "analyst": "analyst1",
    "likes":1,
    "expression_hash": "expression_hash1",
    "dataset_id": 1,
}

entries.append(
    (ClusterSolution, one_cluster_solution)
)
'''id	name	label	description	cluster_solution_id
1	cluster1	label1	description1	1
2	cluster2	label2	description2	1'''

one_cluster = {
    "id": 1,
    "name" : "cluster1",
    "label" : "label1",
    "description": "description1",
    "cluster_solution_id": 1,
"cell_count":1
}

entries.append(
    (Cluster, one_cluster)
)

two_cluster = {
    "id": 2,
    "name" : "cluster2",
    "label" : "label2",
    "description": "description2",
    "cluster_solution_id": 1,
    "cell_count":1
}

entries.append(
    (Cluster, two_cluster)
)

'''id	name	cluster_id
1	sample1	1
2	sample2	2'''

one_cell = {
    "id": 1,
    "name": "sample1",
    "cluster_id": 1
}

entries.append(
    (CellAssignment, one_cell)
)

two_cell = {
    "id": 2,
    "name": "sample2",
    "cluster_id": 2
}

entries.append(
    (CellAssignment, two_cell)
)
