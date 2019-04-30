--DROP TABLE IF EXISTS gene_of_set;
--DROP TABLE IF EXISTS gene_set;
--DROP TABLE IF EXISTS cluster_attribute;
--DROP TABLE IF EXISTS cell_of_cluster;
--DROP TABLE IF EXISTS cluster;
--DROP TABLE IF EXISTS cluster_solution;
--DROP TABLE IF EXISTS dataset;

CREATE TABLE IF NOT EXISTS dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    uuid text,
    species text,
    organ text,
    cell_count INTEGER,
    disease text,
    platform text,
    description text,
    data_source_url text,
    publication_url text
);
CREATE TABLE IF NOT EXISTS cluster_solution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    description text,
    method text,
    method_implementation text,
    method_url text,
    method_parameters text,
    scores text,
    analyst text,
    analyst_favorite INTEGER,
    likes INTEGER,
    expression_hash text,
    dataset_id INTEGER NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES dataset(id)
);
CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    label text,
    description text,
    cluster_solution_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_solution_id) REFERENCES cluster_solution(id)
);
CREATE TABLE IF NOT EXISTS cell_of_cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    cluster_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_id) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS cluster_attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    value text,
    cluster_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_id) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS gene_set (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    type text NOT NULL,
    method text,
    cluster_solution_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_solution_id) REFERENCES cluster_solution(id)
);
CREATE TABLE IF NOT EXISTS gene_of_set (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    gene_set_id INTEGER NOT NULL,
    FOREIGN KEY(gene_set_id) REFERENCES gene_set(id)
);
