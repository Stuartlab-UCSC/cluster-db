from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy.orm import relationship

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship
Model = db.Model
backref = db.backref
ForeignKey = db.ForeignKey
relationship = db.relationship


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """
    __bind_key__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))

