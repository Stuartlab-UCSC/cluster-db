
# Authorization query listener that listens to each query and applies a filter
# so that the user only sees data containing a role she has.

# The code is currently not used so is commented out, and could be possibly used in the future...
'''
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.interfaces import MapperOption
from sqlalchemy import Column, String


@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    """A query compilation rule that will add limiting criteria for every
    query when the RoleOption is used"""

    for opt in query._with_options:
        if isinstance(opt, RoleOption):
            user_roles = opt.user_roles # a list of the user's roles

            # tell Query to definitely repopulate everything.
            # this also clears "sticky" MapperOption objects that may
            # be associated with existing objects
            query = query.populate_existing()

            break
    else:
        # no criteria located, do nothing
        return query

    for ent in query.column_descriptions:
        entity = ent['entity']
        if entity is None:
            continue
        insp = inspect(ent['entity'])
        mapper = getattr(insp, 'mapper', None)
        if mapper and issubclass(mapper.class_, HasRole):
            print("ent['entity'].role:", ent['entity'].role)
            query = query.enable_assertions(False).filter(
                ent['entity'].role == 'none')
                #ent['entity'].role.in_((user_roles)))
                #ent['entity'].role.in_((user_roles))).all()

                #.filter(MyUserClass.id.in_((123,456))).all()
                    #https://stackoverflow.com/questions/8603088/sqlalchemy-in-clause
                    
            # original:
            #query = query.enable_assertions(False).filter(
            #    ent['entity'].timestamp.between(lower, upper))

    return query


class HasRole(object):
    """Mixin that identifies a class as having a role column for authorization"""

    role = Column(String)
    #timestamp = Column(
    #    DateTime, default=datetime.datetime.utcnow, nullable=False)


class RoleOption(MapperOption):
    """A MapperOption that specifes auth roles to apply to a query."""
    propagate_to_loaders = True

    def __init__(self, user_roles):
        self.user_roles = user_rolescd
'''