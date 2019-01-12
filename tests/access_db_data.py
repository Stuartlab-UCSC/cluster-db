

accept_tsv = 'text/tsv'
accept_json = 'application/json'
json_headers = {
    'Content-Type': accept_json,
    'Accept': accept_json
}
tsv_headers = {
    #'Content-Type': accept_tsv,
    'Accept': accept_tsv
}

add_one_dataset = {
    "name": "dataset1",
    "species": "dog"
}
add_second_dataset = {
    "name": "dataset2",
    "species": "cat"
}
add_third_dataset = {
    "name": "dataset3",
    "species": "dog"
}
'''
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
'''
add_one_clustering_solution = {
    "name": "clustering_solution1",
    "method": "method1",
    "method_implementation": "method_implementation1",
    "method_url": "method_url1",
    "method_parameters": "method_parameters1",
    "analyst": "analyst1",
    "secondary": 0,
    "dataset": "dataset1",
}
add_second_clustering_solution = {
    "name": "clustering_solution2",
    "method": "method2",
    "method_implementation": "method_implementation2",
    "method_url": "method_url2",
    "method_parameters": "method_parameters2",
    "analyst": "analyst2",
    "secondary": 1,
    "dataset": "dataset1",
}
add_one_signature_gene_set = {
    "name": "signature_gene_set1",
    "method": "method1",
    "clustering_solution": "clustering_solution1"
}
add_second_signature_gene_set = {
    "name": "signature_gene_set2",
    "method": "method2",
    "clustering_solution": "clustering_solution1"
}
add_one_signature_gene = {
    "name": "signature_gene1",
    "signature_gene_set": "signature_gene_set1"
}
add_second_signature_gene = {
    "name": "signature_gene2",
    "signature_gene_set": "signature_gene_set1"
}
add_one_cluster = {
    "name": "cluster1",
    "clustering_solution": "clustering_solution1"
}
add_second_cluster = {
    "name": "cluster2",
    "clustering_solution": "clustering_solution1"
}
add_one_attribute = {
    "name": "attribute1",
    "value": "value1",
    "cluster": "cluster1"
}
add_second_attribute = {
    "name": "attribute2",
    "value": "value2",
    "cluster": "cluster1"
}
add_second_attribute = {
    "name": "attribute2",
    "value": "value2",
    "cluster": "cluster1"
}
add_one_cluster_assignment = {
    "name": "sample1",
    "cluster": "cluster1"
}
add_second_cluster_assignment = {
    "name": "sample2",
    "cluster": "cluster1"
}
