
# api/cluster_assignment.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cluster_assignment_table \
    import cluster_assignment as table

table_name = 'cluster_assignment'
ns = api.namespace('cluster_assignment')
model = api.model('cluster_assignment', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})

# Just debugging:
#filename = "cluster/api/common/get_all.py"
#exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api/common/add_tsv_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = \
    "cluster/api/common/get_by_clustering_solution.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

"""
filename = "cluster/api/common/delete.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))

filename = "cluster/api/common/update.py"
exec(compile(source=open(filename).read(), filename='filename', mode='exec'))
"""
