
# api/cluster_assignment.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cluster_assignment_table import cluster_assignment as table

table_name = 'cluster_assignment'
ns = api.namespace('cluster_assignment')
model = api.model('cluster_assignment', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})


# Add many from TSV file.
@ns.route('/add_many/tsv_file/<string:tsv_file>/cluster/<string:cluster_name>')
@ns.param('tsv_file', 'TSV file path')
@ns.param('cluster_name', 'Cluster these belong to')
class Add_many_tsv_file(Resource):
    @ns.response(200, 'Success with row count of added')
    def get(self, tsv_file, cluster_name):
        '''ADD MANY FROM TSV FILE'''
        return table.add_many_tsv(tsv_file, cluster_name)


# Get rows by parent (foreign key) name.
@ns.route('/get_by_cluster/<string:cluster_name>')
@ns.param('cluster_name', 'name of parent cluster')
class Get_by_parent(Resource):
    @ns.response(200, 'list of ' + table_name + 's in JSON or TSV format')
    def get(self, cluster_name):
        '''GET BY CLUSTER'''
        return table.get_by_parent(cluster_name, request.accept_mimetypes)


# Just debugging:
#filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_all.py"
#exec(compile(source=open(filename).read(), filename='filename', mode='exec'))


# Do the equivalent of a bash shell 'source' to get the base routes.
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/add_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/get_one.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
filename = "/Users/swat/dev/cdb/clusterDb/cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
