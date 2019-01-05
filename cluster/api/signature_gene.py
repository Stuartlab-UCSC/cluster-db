
# api/signature_gene.py

from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.signature_gene_table import signature_gene as table

table_name = 'signature gene'
ns = api.namespace('signature_gene')
model = api.model('signature_gene', {
    'name': fields.String(required=True, description='Gene name'),
    'signature_gene_set': fields.String(required=True, description='Name of the signature gene set'),
})


# Get rows by parent (foreign key) name.
@ns.route('/get_by_signature_gene_set/<string:signature_gene_set_name>')
@ns.param('signature_gene_set_name', 'name of parent signature_gene_set')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, signature_gene_set):
        '''GET BY SIGNATURE GENE SET'''
        return table.get_by_parent(signature_gene_set, request.accept_mimetypes)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
