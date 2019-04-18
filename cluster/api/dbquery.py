"""
Information retrieval from the db.
"""
from cluster.database.models import Cluster, ClusterSolution, Marker, Dataset, CellAssignment
from cluster.database import db
from sqlalchemy import or_, func

import pandas as pd
import os


def one_marker():
    return help(Marker.query)


def get_dataset_name(id):
    return Dataset.query.get(id).name


def get_cluster_solution_name(id):
    return ClusterSolution.query.get(id).name


def get_cluster_name(id):
    return Cluster.query.get(id).name


def key_maker(*args):
    return "-::-:".join(args)


def key_splitter(key):
    keys = key.split("-::-:")
    return keys


def all_for_marker(marker_name, variable):
    query = db.session.query(Marker).filter(
        or_(
            Marker.hugo_name == marker_name,
            Marker.ensembl_name == marker_name
        )
    )
    # Hacky way to organize the database query into the expected response structure.
    # A better way would be to use a groupby dataset_name and cluster_solution_name (TODO)
    # i'd hope that would be more efficient.
    qdicts = [
            {"dataset_name": get_dataset_name(q.dataset_id),
             "cluster_solution_name": get_cluster_solution_name(q.cluster_solution_id),
             "cluster_name": get_cluster_name(q.cluster_id),
             "value": q.__dict__[variable]
             } for q in query
    ]

    dict_lookup = {}
    for d in qdicts:
        try:
            key = key_maker(d["dataset_name"], d["cluster_solution_name"])
            dict_lookup[key] += [{"name": d["cluster_name"], "value": d["value"]}]
        except KeyError:
            dict_lookup[key] = [{"name": d["cluster_name"], "value": d["value"]}]


    resp = []
    for key in dict_lookup.keys():
        dataset_name, cluster_solution_name = key_splitter(key)
        resp += [{"dataset_name": dataset_name, "cluster_solution_name": cluster_solution_name, "clusters": dict_lookup[key]}]

    return {"gene": marker_name, "variable": variable, "cluster_solutions": resp}


def cell_count_of_cluster(cluster_id):
    return Cluster.query.get(cluster_id).cell_count


def all_for_marker_dotplot(marker_name, size_var, color_var):
    query = db.session.query(Dataset.name, ClusterSolution.name, Cluster.name, Cluster.cell_count, Marker, Dataset.species, Dataset.organ) \
        .filter(
            or_(
                func.upper(Marker.hugo_name) == func.upper(marker_name),
                Marker.ensembl_name == marker_name
            )
        ).filter(
          Dataset.id == Marker.dataset_id
        ).filter(
            ClusterSolution.id == Marker.cluster_solution_id
        ).filter(
            Cluster.id == Marker.cluster_id
        ).subquery()

    df = pd.read_sql(query, db.engine.connect())
    new_names = ["dataset_name", "cluster_solution_name", "cluster_name"]
    new_names.extend(df.columns[3:])
    df.columns = new_names

    marker_dicts = {"gene": marker_name, "size_by": size_var, "color_by": color_var, "cluster_solutions": []}
    a = df.groupby(by=["dataset_id","cluster_solution_id"])
    for name, group in a:
        dataset_name = group["dataset_name"].iloc[0]
        organ = group["organ"].iloc[0]
        if organ is None:
            organ = "undetermined"
        cluster_solution_name = group["cluster_solution_name"].iloc[0]
        species_name = group["species"].iloc[0]


        group = group[[size_var, color_var, "cluster_name", "cell_count"]]
        #print(group.head())
        group.columns = ["size", "color", "name", "cell_count"]
        group = group.fillna(0)
        cluster_dicts = group.to_dict(orient="records")
        # Add to the clustering solutions
        marker_dicts["cluster_solutions"].append(
            {
                "dataset": {
                    "name": dataset_name,
                    "species": species_name,
                    "organ": organ,
                    "study": "not recorded"
                },
                "dataset_name": dataset_name,
                "cluster_solution_name": cluster_solution_name,
                "clusters": cluster_dicts
            }

        )

    return marker_dicts


def one_cluster_solution():
    return db.session.query(ClusterSolution).get(5) #.query.filter_by(id = 1).one()


def get_marker_set(cell_type, cluster_solution_name):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataset_name = "fetal combined heart of cells"
    cluster_solution_name = "heart cell types"
    size = "similarity"

def cluster_similarity2(color=None, cell_type_name="invivo-hand-curated"):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataset_name = "fetal combined heart of cells"
    cluster_solution_name = "heart cell types"
    size = "percent_marker_expression"
    color = "percent_marker_expressoin"


    corrs = pd.read_csv(os.path.join(dirname, "corrs.invivo-celltype.invitro-res-04.csv"), index_col=0)

    focus_cell_types = [ct for ct in corrs if ct not in color_centroids.index]
    query_cell_types = color_centroids.index

    other_dataset = "in vitro combined heart of cells"
    other_species = "human"
    other_study = "in vitro"
    other_organ = "heart"
    other_cluster_solution_name = "louvain resolution 0.4"
    big_dict = {
        "dataset_name": dataset_name,
        "cluster_solution_name": cluster_solution_name,
        "size_by": size,
        "color_by": color,
        "cluster_similarities": []
    }

    for celltype in focus_cell_types:
        cs_dict = {
            "dataset": {
                "name": other_dataset,
                "species": other_species,
                "organ": other_organ,
                "study": other_study
            },
            "compared_to_cluster": celltype,
            "cluster_solution_name": other_cluster_solution_name,
            "clusters": []

        }
        for cluster in query_cell_types:
            cluster_dict = {
                "name": cluster,
                "size": corrs.loc[celltype, cluster].item(),
                "color": color_centroids[cluster].item(),
                "cell_count": cluster_cell_counts.loc[int(cluster)].item()
            }
            cs_dict["clusters"].append(cluster_dict)

        big_dict["cluster_similarities"].append(cs_dict)

    return big_dict

def cluster_similarity(cluster_solution_name, gene_name="MYL7"):
    dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data")
    dataset_name = "Mock heart of cells project"
    cluster_solution_name = "heart cell types"
    size = "similarity"
    color = gene_name
    #print("hlleo")
    #corrs = pd.read_csv(os.path.join(dirname, "corrs.invivo-celltype.invitro-res-04.csv"), index_col=0)
    corrs = pd.read_csv(os.path.join(dirname, "test.csv"), index_col=0)
    corrs = corrs.fillna(1)
    corrs.index = [str(i) for i in corrs.index]
    color_centroids = pd.read_csv(os.path.join(dirname,"invitroCombined.res_0_4.centroids.csv"), index_col=0).loc[color]
    cluster_cell_counts = pd.read_csv(os.path.join(dirname,"invitroCombined.cluster.cellcounts.csv"), index_col=0)


    #focus_cell_types = [ct for ct in corrs if ct not in color_centroids.index]
    focus_cell_types = corrs.index#[ct for ct in corrs if ct not in color_centroids.index]
    query_cell_types = color_centroids.index

    other_dataset = "user supplied cluster solution"
    other_species = "human"
    other_study = "in vitro"
    other_organ = "heart"
    other_cluster_solution_name = "louvain resolution 0.4"
    big_dict = {
        "dataset_name": dataset_name,
        "cluster_solution_name": cluster_solution_name,
        "size_by": size,
        "color_by": color,
        "cluster_similarities": []
    }
    #print(corrs.head())
    #print(query_cell_types)
    #print(focus_cell_types)
    for celltype in focus_cell_types:
        cs_dict = {
            "dataset": {
                "name": other_dataset,
                "species": other_species,
                "organ": other_organ,
                "study": other_study
            },
            "compared_to_cluster": celltype,
            "cluster_solution_name": other_cluster_solution_name,
            "clusters": []

        }
        for cluster in query_cell_types.tolist():
            #print(cluster)
            cluster_dict = {
                "name": cluster,
                "size": corrs.loc[celltype, cluster].item(),
                "color": color_centroids[cluster].item(),
                "cell_count": cluster_cell_counts.loc[int(cluster)].item()
            }

            cs_dict["clusters"].append(cluster_dict)

        #print(cs_dict)
        big_dict["cluster_similarities"].append(cs_dict)

    #print(len(big_dict["cluster_similarities"]))
    #print(big_dict)
    return big_dict