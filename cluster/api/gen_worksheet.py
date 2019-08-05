
"""
Temporary place for unused code.
"""

def generate_worksheet(user, worksheet):
    """Generates a worksheet on the fly."""

    marker_dicts = read_json_gzipd(TEST_MARKERS_DICT_PATH)['markers']

    cluster_solution_name = CLUSTER_SOLUTION_NAME

    genes = find_genes(marker_dicts, cluster_solution_name=cluster_solution_name)

    colors = bubble_table(
        marker_dicts,
        genes.tolist(),
        cluster_solution_name=cluster_solution_name,
        attr_name="z_stat"
    )

    sizes = bubble_table(
        marker_dicts,
        genes.tolist(),
        cluster_solution_name=cluster_solution_name,
        attr_name="specificity"
    )

    gene_table_url = url_for(
        'api.user_gene_table',
        user=user,
        worksheet=worksheet,
        cluster_name=DEFAULT_CLUSTER_SOLUTION,
        _external=True
    )

    scatterplot_url = url_for(
        'api.user_cluster_scatterplot',
        user=user, worksheet=worksheet,
        type=DEFAULT_SCATTER_TYPE,
        _external=True
    )

    resp = {
        "user": "tester", "worksheet": "test",
        "dataset_name": "krigstien6K-fastfood",
        "size_by": "percent expressed",
        "color_by": "z statistic",
        "clusters": dataframe_to_str(pd.read_csv(TEST_CLUSTER_TABLE_PATH, sep="\t"), index=False),
        "genes": dataframe_to_str(genes),
        "colors": dataframe_to_str(colors),
        "sizes": dataframe_to_str(sizes),
        "gene_table_url": gene_table_url,
        "scatterplot_url": scatterplot_url
    }
    return resp
