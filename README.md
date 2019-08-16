# cluster-db
This is the backend for the [UCSC's Cell Atlas](https://cellatlas.ucsc.edu/). It does handy things like exposing single cell clustering solutions
to the community via a RESTful api, and stores the Cell Type Worksheets of our users. Have a peak at the [swagger docs](https://cellatlasapi.ucsc.edu/)
or check out the front-end application for [Cell Type Worksheets](https://cellatlas.ucsc.edu/cell-type).


### Install

Our current path for installation is to clone the git repository and work inside a python virtual environment.

Python3.6+, pip, virtualenv, and github are required for the installation.
```
cd path/to/work/dir

git clone https://github.com/stuartlab-UCSC/cluster-db

cd cluster-db

virtualenv -p python3 env

source env/bin/activate

pip install -r requirements.txt
```
Now you've installed the app and it's dependencies.

If the install has gone correctly you should be able to view the command line interface documentation.
```
source env/bin/activate
export FLASK_APP=cluster
# List all high-level functions
flask --help
# Get documentation for a specific function
flask create-worksheet --help
```
To run the server locally use flask's api:
```
source env/bin/activate
export FLASK_APP=cluster
flask run -h localhost -p 5555 --with-threads
```
You can now interact with your local installation via the swagger docs at http://localhost:5555

If you're interested in running the server as a https background process, create a configuration file named clusterDbConfig.sh
in the cluster-db directory. Here's an example:

```
export BACKGROUND=1
export HOST=localhost
export PORT=9000
export HTTPS=1
# Set this if you are also running the client side of the application.
export VIEWER_URL=https://cellatlas.ucsc.edu/
export WWW_SOCKET=127.0.0.1:$PORT
# Expose machine specific security variables to the environment.
source /<protected-dir>/security-variables
source $CLUSTERDB/
```
Now you can start the app via our start script from the cluster-db directory:
```
cd path/cluster-db
export CLUSTERDB=$(pwd)
bin/start
```
To see the database from the front-end you will need to follow the installation instructions for the [USCS Cell Atlas](https://github.com/Stuartlab-UCSC/cell-atlas). 
