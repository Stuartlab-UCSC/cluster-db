
--DROP TABLE IF EXISTS dataset;
--DROP TABLE IF EXISTS clustering;
--DROP TABLE IF EXISTS signature_gene_set;
--DROP TABLE IF EXISTS signature_gene;


CREATE TABLE IF NOT EXISTS dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    species text NOT NULL,
    organ text,
    sampleCount INTEGER,
    abnormality text,
    primaryData text,
    scanpyObjectOfPrimaryData text,
    sampleMetadata text,
    primaryDataNormalizationStatus text,
    clusteringScript text,
    reasonableForTrajectoryAnalysis INTEGER,
    trajectoryAnalysisScript text,
    platform text,
    expressionDataSource text,
    expressionDataSourceURL text
);

CREATE TABLE IF NOT EXISTS clustering (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    method text,
    method_implementation text,
    method_url text,
    method_parameters text,
    analyst text,
    secondary INTEGER,
    dataset_id INTEGER,
    FOREIGN KEY(dataset_id) REFERENCES dataset(id)
);

CREATE TABLE IF NOT EXISTS signature_gene_set (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    method text,
    clustering_id INTEGER,
    FOREIGN KEY(clustering_id) REFERENCES clustering(id)
);
/*
CREATE TABLE IF NOT EXISTS signature_gene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    signature_gene_set_id INTEGER NOT NULL,
        CONSTRAINT fk_signature_gene_set
        FOREIGN KEY (signature_gene_set_id)
        REFERENCES signature_gene_set(id)
);
*/
/*
CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    clustering_id INTEGER NOT NULL REFERENCES clustering(id)
);
CREATE TABLE IF NOT EXISTS cluster_assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample text UNIQUE NOT NULL,
    cluster_id INTEGER NOT NULL REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    value text,
    cluster_id INTEGER NOT NULL REFERENCES cluster(id)
);
*/