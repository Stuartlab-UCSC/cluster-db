--DROP TABLE IF EXISTS clustering;

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
    dataset INTEGER,
    FOREIGN KEY(dataset) REFERENCES dataset(id)
);
CREATE TABLE IF NOT EXISTS signature_gene_set (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    method text,
    clustering INTEGER,
    FOREIGN KEY(clustering) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS signature_gene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    signature_gene_set INTEGER,
    FOREIGN KEY(signature_gene_set) REFERENCES signature_gene_set(id)
);

/*
CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    clustering INTEGER,
    FOREIGN KEY(clustering) REFERENCES clustering(id)
);
CREATE TABLE IF NOT EXISTS cluster_assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample text UNIQUE NOT NULL,
    cluster INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    value text,
    cluster INTEGER,
    FOREIGN KEY(cluster) REFERENCES cluster(id)
);
*/