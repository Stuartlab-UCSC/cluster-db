
# api/cell_assignment.py

from flask import request
from flask_restplus import fields,  Resource
from cluster.api.restplus import api
from cluster.database.cell_assignment_table \
    import cell_assignment as table

table_name = 'cell_assignment'
ns = api.namespace('cell_assignment')
model = api.model('cell_assignment', {
    'name': fields.String(required=True, description='Sample name'),
    'cluster': fields.String(required=True, description='Name of the cluster'),
})

