
# api/cluster_assignment.py

from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cluster_assignment_table import cluster_assignment as table

table_name = 'cluster_assignment'
ns = api.namespace('cluster_assignment')
model = api.model('cluster_assignment', {
    'sample': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})


# Get rows by parent (foreign key) name.
@ns.route('/get_by_cluster/<string:cluster_name>')
@ns.param('cluster_name', 'name of parent cluster')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, cluster):
        '''GET BY CLUSTERING SOLUTION'''
        return table.get_by_parent(cluster, request.accept_mimetypes)


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
