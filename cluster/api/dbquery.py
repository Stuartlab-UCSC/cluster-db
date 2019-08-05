"""
Databast queries wrangled into expected formats.
"""
from cluster.database.data_models import Cluster, ClusterSolution, Marker, Dataset, CellAssignment
from cluster.database import db
from sqlalchemy import or_, and_, func
import pandas as pd


def all_datasets():
    """All data sets from the data set table."""
    query = db.session.query(Dataset)
    result = [dict(name=q.name, description=q.description, id=q.id) for q in query]
    return result


def cluster_solutions(dataset_id):
    """Return all cluster solutions available for a given data set id."""
    query = db.session.query(ClusterSolution).filter(ClusterSolution.dataset_id == dataset_id)

    result = [dict(name=q.name, method=q.method, id=q.id) for q in query]
    return result


def cell_assignments(cluster_solution_id):
    """Return all cell assignments to clusters for a given cluster solution id."""
    query = db.session.query(Cluster, CellAssignment)\
        .filter(Cluster.cluster_solution_id == cluster_solution_id)\
        .filter(Cluster.id == CellAssignment.cluster_id)

    result = [dict(name=q[1].name, cluster_name=q[0].name) for q in query]

    return result


def cluster_solution_id(dataset_name, cluster_solution_name):
    """Get a cluster_solution_id from dataset name and cluster solution name."""
    dataset_id = get_dataset(name=dataset_name).id
    cs_id = db.session.query(ClusterSolution)\
        .filter(
            and_(
                ClusterSolution.dataset_id == dataset_id,
                ClusterSolution.name == cluster_solution_name
            )
        )[0].id
    return cs_id


def get_dataset(id=None, name=None):
    """Get a dataset by name or id."""
    query = db.session.query(Dataset).\
        filter(
        or_(
            Dataset.id == id,
            Dataset.name == name
        )
    )[0]
    return query


def get_cluster_solution_name(id):
    return ClusterSolution.query.get(id).name


def get_cluster_name(id):
    return Cluster.query.get(id).name


def cell_count_of_cluster(cluster_id):
    return Cluster.query.get(cluster_id).cell_count


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
            {"dataset_name": get_dataset(id=q.dataset_id).name,
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


def key_maker(*args):
    return "-::-:".join(args)


def key_splitter(key):
    keys = key.split("-::-:")
    return keys

