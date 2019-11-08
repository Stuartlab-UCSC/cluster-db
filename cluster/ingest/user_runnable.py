"""
Entry point for user-runnable scripts.
"""

from cluster.ingest.main import ingest_scanpy

def load_scanpy(user_email, worksheet_name, scanpy_path, cluster_name='',
    dataset_name='', size_by="zstat", color_by="tstat", celltype_key=None):
    
    (xys, exp, clustering, markers) =
        ingest_scanpy(user_email, worksheet_name, scanpy_path, cluster_name,
        dataset_name, size_by, color_by, celltype_key)
        
    #write_all_upload_data(user_email, worksheet_name, xys=xys, exp=exp,
    #    clustering=clustering, markers=markers_df)

