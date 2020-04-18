# cluster-db
This is the backend for the [UCSC's Cell Atlas](https://cellatlas.ucsc.edu/). It does handy things 
like exposing single cell clustering solutions
to the community via a RESTful api, and stores the Cell Type Worksheets of our users. Have a 
peak at the [swagger docs](https://cellatlasapi.ucsc.edu/)
or check out the front-end application for 
[Cell Type Worksheets](https://cellatlas.ucsc.edu/cell-type).


## Install

Our current path for installation is to clone the git repository and work inside a python virtual 
environment.

Python3.6+, pip, virtualenv, and github are required for the installation.
```
cd path/to/work/dir

git clone https://github.com/stuartlab-UCSC/cluster-db.git

cd cluster-db

mkdir instance

virtualenv -p python3 instance/env

source instance/env/bin/activate

pip install -r requirements.txt

export CLUSTERDB=full.path.to.your.git.install.directory
```
Now you've installed the app and it's dependencies.

## Start
To run the server locally use flask's api:
```
cd $CLUSTERDB
bin/start
```
You can now interact with your local installation via the swagger docs at 
http://localhost:5555

If you're interested in running the server as a https background process, 
create a configuration file named clusterDbConfig.sh
in the cluster-db directory. Here's an example:

```
export FLASK_APP=cluster
export BACKGROUND=1
export FLASK_DEBUG=True # TODO turn off for production
export FLASK_ENV=development # TODO turn off for production
export HOST=localhost
export PORT=9000
export HTTPS=1
# Set this if you are also running the web client side of the application.
export VIEWER_URL=https://cellatlas.ucsc.edu/
export WWW_SOCKET=127.0.0.1:$PORT
# Expose machine specific security variables to the environment.
source /<protected-dir>/security-variables
source $CLUSTERDB/instance/env/bin/activate
```
Now you can start the app as above.

## Stop
```
ps -eaf | grep flask
```
Kill the lowest process number for the flask process running.


## Run CLI commands:
```
cd $CLUSTERDB
source bin/startCli
```

## Instance files
Your config, database, and uploaded cell type worksheets ingest data will be in 
$CLUSTERDB/instance. If you want them somewhere else, make a symbolic link of 'instance'
to point to your instance-specific directory.

## Front-end
To see the database from the front-end you will need to follow the installation instructions for 
the [UCSC Cell Atlas](https://github.com/Stuartlab-UCSC/cell-atlas). 
