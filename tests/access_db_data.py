
import json

text_plain = 'text/plain; charset=utf-8'

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
add_third_clustering_solution = {
    "name": "clustering_solution2",
    "method": "method3",
    "method_implementation": "method_implementation3",
    "method_url": "method_url3",
    "method_parameters": "method_parameters3",
    "analyst": "analyst3",
    "secondary": 1,
    "dataset": "dataset2",
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
add_third_signature_gene_set = {
    "name": "signature_gene_set2",
    "method": "method2",
    "clustering_solution": "clustering_solution2"
}


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

