"""
Tests some of the internals that generate the categorical scatter plot
"""
from cluster.api.user import graph_protions, centroids
from tests.gen_data import gen_cluster, gen_expression, gen_xy
from cluster.api.user import join_xys_clusters

def test_centroids():
    n_clusters = 11
    xys, clustering = (gen_xy(), gen_cluster(n_clusters=n_clusters))
    c = centroids(xys, clustering)
    assert c.shape[0] == 11
    assert c.index.dtype == 'object'


def test_graph_proportions():
    xys, clustering, expression = (gen_xy(), gen_cluster(n_clusters=3), gen_expression())

    colormap = dict(zip(clustering.unique().tolist(), ["black", "white", "yellow"]))
    centers = centroids(xys, clustering)

    data = join_xys_clusters(xys, clustering)

    for xs, ys, cx, cy, color, label in graph_protions(centers, data, colormap):

        got_values = len(xs) and len(ys)
        got_centers = isinstance(cx, float) and isinstance(cy, float)
        got_label = isinstance(label, str)
        got_color = isinstance(color, str)

        assert got_values
        assert got_centers
        assert got_label
        assert got_color


def test_join_xys_clusters():
    n_samples = 100
    xys, clustering = (gen_xy(n_samples), gen_cluster(n_clusters=3))

    df = join_xys_clusters(xys, clustering)
    assert df.shape[1] == 3
    assert df["cluster"].dtype == "object"
    assert df.shape[0] == n_samples