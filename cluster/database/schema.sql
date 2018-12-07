-- DROP TABLE IF EXISTS clustering;

CREATE TABLE IF NOT EXISTS dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    species text NOT NULL,
    organ text,
    sampleCount integer,
    abnormality text,
    primaryData text,
    scanpyObjectOfPrimaryData text,
    sampleMetadata text,
    primaryDataNormalizationStatus text,
    clusteringScript text,
    reasonableForTrajectoryAnalysis bool,
    trajectoryAnalysisScript text,
    platform text,
    expressionDataSource text,
    expressionDataSourceURL text
);
CREATE TABLE IF NOT EXISTS clustering (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    method text,
    method_url text,
    method_parameters text,
    analyst text,
    secondary bool,
    dataset INTEGER,
    FOREIGN KEY(dataset) REFERENCES dataset(id)
);
CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    clustering,
    FOREIGN KEY(clustering) REFERENCES clustering(id)
);
CREATE TABLE IF NOT EXISTS marker_gene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    cluster INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS ranked_gene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    rank INTEGER,
    cluster INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS gene_module (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    descr text,
    gene_count INTEGER
);
CREATE TABLE IF NOT EXISTS ranked_gene_module (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    rank INTEGER,
    cluster INTEGER,
    gene_module INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id),
    FOREIGN KEY(gene_module) REFERENCES gene_module(id)
);
CREATE TABLE IF NOT EXISTS gene_of_module (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    gene_module INTEGER,
    FOREIGN KEY(gene_module) REFERENCES gene_module(id)
);
CREATE TABLE IF NOT EXISTS attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    value text,
    cluster INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id)
);
