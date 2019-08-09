from flask_restplus import  Resource
from cluster.api.restplus import api
from cluster.scorect import _score_celltypes
import pandas as pd
from cluster.api.user import parse_genes

ns = api.namespace('scorect')


def read_markers_gmt(filepath):
    """
    Read a marker file from a gmt.
    """
    from collections import OrderedDict
    ct_dict = OrderedDict()
    with open(filepath) as file_gmt:
        for line in file_gmt:
            values = line.strip().split('\t')
            ct_dict[values[0]] = values[2:]
    return ct_dict


def get_celltype_markers():
    return read_markers_gmt("all_celltypes.gmt")


def get_background():
    return pd.read_csv("background_genes.lst", header=None)[0].tolist()

from cluster.utils import timeit

@ns.route('/genes/<string:genes>')
@ns.param('genes', 'comma separated hugo genes, e.g. TP53,ALKBH6,ALKBH4')
class ScoreCT(Resource):
    @timeit(id_string="score ct get")
    @ns.response(200, 'cell type')
    def get(self, genes):
        """Most likely cell type given a set of genes."""
        genes = parse_genes(genes)
        ct_markers = get_celltype_markers()
        cell_types = ct_markers.keys()
        #print(ct_markers.shape)
        #ct_markers.to_pickle("all_celltype_ref_df.pi")
        background = get_background()

        print("genes in background: %d out of %d" % (len(set(genes).intersection(set(background))), len(genes)))
        scores, pvals = _score_celltypes(1, ct_markers["pca - cell cycle"][-3:], ct_markers, get_background(), [1])
        print("sig", (pvals < .05).sum())
        pvals = pd.Series(pvals, index=cell_types)
        print(pvals.index[(pvals < .05)])
        print(pd.Series(pvals, index=cell_types).idxmin(), pd.Series(pvals, index=cell_types).min())
        #print(pvals)
        return None
