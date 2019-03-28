from cluster.database.models import Cluster, ClusterSolution, Marker, Dataset, CellAssignment
from cluster.database import db
from sqlalchemy import or_




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
    return db.session.query(CellAssignment).filter(CellAssignment.cluster_id == cluster_id).count()


def all_for_marker_dotplot(marker_name, size_var, color_var):
    query = db.session.query(Marker).filter(
        or_(
            Marker.hugo_name == marker_name,
            Marker.ensembl_name == marker_name
        )
    )
    # Hacky way to organize the database query into the expected response structure.
    # Esseentially we are using a dict and some manufactured keys to do a groupby statement.
    # A better way might be to use sql groupby functionality  on dataset_name and cluster_solution_name (TODO)
    # i'd hope that would be more efficient.
    # TODO the cluster model needs to have a cell count field so we don't have to do an expensive count
    cluster_ids = list(
        set(
            [q.cluster_id for q in query]
        )
    )
    cell_count_lookup = dict(zip(cluster_ids, [cell_count_of_cluster(cid) for cid in cluster_ids]))

    qdicts = [
        {"dataset_name": get_dataset_name(q.dataset_id),
         "cluster_solution_name": get_cluster_solution_name(q.cluster_solution_id),
         "cluster_name": get_cluster_name(q.cluster_id),
         "size": q.__dict__[size_var],
         "color": q.__dict__[color_var],
         "cell_count": cell_count_lookup[q.cluster_id]
         } for q in query
    ]

    dict_lookup = {}
    for d in qdicts:
        try:
            key = key_maker(d["dataset_name"], d["cluster_solution_name"])
            dict_lookup[key] += [
                {"name": d["cluster_name"],
                 "size": d["size"],
                 "color": d["color"],
                 "cell_count": d["cell_count"]
                 }
            ]
        except KeyError:
            dict_lookup[key] = [
                {"name": d["cluster_name"],
                 "size": d["size"],
                 "color": d["color"],
                 "cell_count": d["cell_count"]
                 }
            ]

    resp = []
    for key in dict_lookup.keys():
        dataset_name, cluster_solution_name = key_splitter(key)
        resp += [{"dataset_name": dataset_name, "cluster_solution_name": cluster_solution_name,
                  "clusters": dict_lookup[key]}]

    print("done")
    return {"gene": marker_name, "size_by": size_var, "color_by": color_var, "cluster_solutions": resp}


def one_cluster_solution():
    return db.session.query(ClusterSolution).get(5) #.query.filter_by(id = 1).one()