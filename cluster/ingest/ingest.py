"""
"""
import os
import cluster.cli.scanpyapi as ad_obj
import numpy as np

def ingest_scanpy(user_email, worksheet_name, scanpy_path, cluster_name,
    dataset_name, size_by, color_by, celltype_key):
    
    print("reading in data...")
    ad = ad_obj.readh5ad(scanpy_path)
    mapping = ad_obj.celltype_mapping(ad, cluster_name, celltype_key)
    use_raw = ad_obj.has_raw(ad)
    xys = ad_obj.get_xys(ad, key="X_umap")

    from cluster.ingest.marker_vals_from_anndata import run_pipe
    markers_df = run_pipe(ad, cluster_name)
    clustering = ad_obj.get_obs(ad, cluster_name)

    #print(ad.var_names)
    # Need to use all of the genes of NA's will come about in the data.

    genes = []

    exp = ad_obj.get_expression(ad, use_raw)
