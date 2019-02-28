
import json

text_plain = 'text/plain; charset=utf-8'

add_one_dataset = {
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
add_second_dataset = {
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
add_third_dataset = {
    "name": "dataset3",
    "uuid": "uuid3",
    "species": "dog",
    "organ": "organ3",
    "cell_count": 3,
    "disease": "disease3",
    "platform": "platform3",
    "description": "description3",
    "data_source_url": "data_source_url3",
    "publication_url": "publication_url3"
}
add_one_cluster_solution = {
    "name": "cluster_solution1",
    "description": "description1",
    "method": "method1",
    "method_implementation": "method_implementation1",
    "method_url": "method_url1",
    "method_parameters": "method_parameters1",
    "scores": "scores1",
    "analyst": "analyst1",
    "analyst_favorite": 1,
    "likes": 1,
    "expression_hash": "expression_hash1",
    "dataset": "dataset1",
}
add_second_cluster_solution = {
    "name": "cluster_solution2",
    "description": "description2",
    "method": "method2",
    "method_implementation": "method_implementation2",
    "method_url": "method_url2",
    "method_parameters": "method_parameters2",
    "scores": "scores2",
    "analyst": "analyst2",
    "analyst_favorite": 0,
    "likes": 2,
    "expression_hash": "expression_hash2",
    "dataset": "dataset1",
}
add_third_cluster_solution = {
    "name": "cluster_solution2",
    "description": "description3",
    "method": "method3",
    "method_implementation": "method_implementation3",
    "method_url": "method_url3",
    "method_parameters": "method_parameters3",
    "scores": "scores3",
    "analyst": "analyst3",
    "analyst_favorite": 1,
    "likes": 3,
    "expression_hash": "expression_hash3",
    "dataset": "dataset2",
}
add_one_gene_set = {
    "name": "gene_set1",
    "type": "signature",
    "method": "method1",
    "cluster_solution": "cluster_solution1"
}
add_second_gene_set = {
    "name": "gene_set2",
    "type": "signature",
    "method": "method2",
    "cluster_solution": "cluster_solution1"
}
add_third_gene_set = {
    "name": "gene_set2",
    "type": "signature",
    "method": "method2",
    "cluster_solution": "cluster_solution2"
}


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

