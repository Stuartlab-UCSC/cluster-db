"""
Provides access to database through sqlalchemy core objects (sqlalchemy.sql.schema.Table) and SQL alchemy ORMs
"""
from cluster.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Dataset(db.Model):
    __tablename__ = "dataset"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    uuid = Column(String)
    species = Column(String)
    organ = Column(String)
    cell_count = Column(Integer)
    disease = Column(String)
    platform = Column(String)
    description = Column(String)
    data_source_url = Column(String)
    publication_url = Column(String)

    def __repr__(self):
     return "<Dataset(name=%s, species=%s, organ=%s, cell count=%d, data source url=%s )>" % \
            (self.name, self.species, self.organ, self.cell_count, self.data_source_url)


class ClusterSolution(db.Model):

    __tablename__ = "cluster_solution"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    method = Column(String)
    method_implementation = Column(String)
    method_url = Column(String)
    method_parameters = Column(String)
    scores = Column(String)
    analyst = Column(String)
    likes = Column(Integer)
    expression_hash = Column(String)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)


class Cluster(db.Model):

    __tablename__ = "cluster"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    label = Column(String)
    description = Column(String)
    cell_count = Column(Integer)
    cluster_solution_id = Column(Integer, ForeignKey("cluster_solution.id"), nullable=False)
    markers = relationship("Marker", backref="Cluster")


class CellAssignment(db.Model):

    __tablename__ = "cell_of_cluster"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cluster_id = Column(Integer, ForeignKey("cluster.id"), nullable=False)


class Marker(db.Model):

    __tablename__ = "marker"

    id = Column(Integer, primary_key=True)
    hugo_name = Column(String)
    ensembl_name = Column(String)
    sensitivity = Column(Float)
    specificity = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    accuracy = Column(Float)
    t_pval = Column(Float)
    z_pval = Column(Float)
    t_stat = Column(Float)
    z_stat = Column(Float)
    log2_fold_change_vs_min = Column(Float)
    log2_fold_change_vs_next = Column(Float)
    mean_expression = Column(Float)
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    cluster_solution_id = Column(Integer, ForeignKey("cluster_solution.id"), nullable=False)
    cluster_id = Column(Integer, ForeignKey("cluster.id"), nullable=False)

    def __repr__(self):

        return("<Marker(name=%s, tstat=%f, mean=%f, log2fc_next=%f)>" %
               (self.hugo_name, self.t_stat, self.mean_expression, self.log2_fold_change_vs_next))
