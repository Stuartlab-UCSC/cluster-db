
--DROP TABLE IF EXISTS dataset;
--DROP TABLE IF EXISTS clustering_solution;
--DROP TABLE IF EXISTS signature_gene_set;
--DROP TABLE IF EXISTS signature_gene;

CREATE TABLE IF NOT EXISTS attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    value text,
    cluster_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_id) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    clustering_solution_id INTEGER NOT NULL,
    FOREIGN KEY(clustering_solution_id) REFERENCES clustering_solution(id)
);
CREATE TABLE IF NOT EXISTS cluster_assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    cluster_id INTEGER NOT NULL,
    FOREIGN KEY(cluster_id) REFERENCES cluster(id)
);
CREATE TABLE IF NOT EXISTS clustering_solution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    method text,
    method_implementation text,
    method_url text,
    method_parameters text,
    analyst text,
    secondary INTEGER,
    dataset_id INTEGER NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES dataset(id)
);
CREATE TABLE IF NOT EXISTS dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE NOT NULL,
    species text NOT NULL
);
--organ text,
--sampleCount INTEGER,
--abnormality text,
--primaryData text,
--scanpyObjectOfPrimaryData text,
--sampleMetadata text,
--primaryDataNormalizationStatus text,
--clusteringScript text,
--reasonableForTrajectoryAnalysis INTEGER,
--trajectoryAnalysisScript text,
--platform text,
--expressionDataSource text,
--expressionDataSourceURL text

CREATE TABLE IF NOT EXISTS signature_gene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    signature_gene_set_id INTEGER NOT NULL,
    FOREIGN KEY(signature_gene_set_id) REFERENCES signature_gene_set(id)
);
CREATE TABLE IF NOT EXISTS signature_gene_set (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    method text,
    clustering_solution_id INTEGER NOT NULL,
    FOREIGN KEY(clustering_solution_id) REFERENCES clustering_solution(id)
);
