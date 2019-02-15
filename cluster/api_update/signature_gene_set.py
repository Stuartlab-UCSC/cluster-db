
# api/signature_gene_set.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.signature_gene_set_table \
    import signature_gene_set as table

table_name = 'signature gene set'
ns = api.namespace('signature_gene_set_update')
model = api.model('signature_gene_set', {
    'name': fields.String(required=True, description='Gene set name'),
    'method': fields.String(required=True, description='Method used to determine this gene set'),
    'cluster_solution': fields.String(required=True, description='Name of the cluster solution'),
})

# Add one by cluster_solution.
@ns.route('/add/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
class Add_many_tsv_file(Resource):
    @ns.expect(model)
    @ns.response(200, 'last database row ID added')
    def post(self, dataset):
        '''ADD ONE'''
        resp = table.add_one(api.payload, [dataset])
        return Response(str(resp), mimetype=mimetype)


# Delete one
@ns.route(
    '/delete/<string:signature_gene_set>' + \
    '/cluster_solution/<string:cluster_solution>' + \
    '/dataset/<string:dataset>')
@ns.param('dataset', 'dataset name')
@ns.param('cluster_solution', 'cluster_solution name')
@ns.param('signature_gene_set', 'signature_gene_set name')
class Delete_by_cluster_solution(Resource):
    @ns.response(200, 'success')
    def get(self, signature_gene_set, cluster_solution, dataset):
        '''DELETE ONE'''
        resp = table.delete_one(signature_gene_set,
            [cluster_solution, dataset])
        return Response(str(resp), mimetype=mimetype)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "cluster/api_update/common/get_all.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api_update/common/get_by_cluster_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

