

accept_tsv = 'text/tsv'
accept_json = 'json/application'

add_one_dataset = {
    "name": "dataset1",
    "species": "dog"
}
add_second_dataset = {
    "name": "dataset2",
    "species": "cat"
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
    "secondary": "secondary1",
    "dataset": "dataset1",
}
add_second_clustering_solution = {
    "name": "clustering_solution2",
    "method": "method2",
    "method_implementation": "method_implementation2",
    "method_url": "method_url2",
    "method_parameters": "method_parameters2",
    "analyst": "analyst2",
    "secondary": "secondary2",
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
    "clustering_solution": "signature_gene_set1"
}
add_second_signature_gene = {
    "name": "signature_gene2",
    "clustering_solution": "csignature_gene_set1"
}
