# clusterDb
RestAPI for single cell clusters.

### Install

You will need to have Python3.7 and Git installed on your machine.

First clone the repo somewhere on your disk.

`cd /path/to/my/workspace/`

`git clone https://github.com/terraswat/clusterDb`


Create a virtual environment and install the requirements.

``virtualenv -p `which python3.7` venv``

`cd clusterDb`

`source ../venv/bin/activate`

`pip install -r requirements.txt`

`deactivate`

`vi ../venv/bin/activate`

Add the following lines to the bottom of the file:
`
export CLUSTERDB=</path/to/my/workspace/>
export CLUSTERDB_HOST=<hostname>
export CLUSTERDB_PORT=<port>
`
for example:
`
export CLUSTERDB=/data/users/swat/dev/cdb
export CLUSTERDB_HOST=hexcalc.ucsc.edu
export CLUSTERDB_PORT=9000
export CLUSTERDB_UPDATABLE=0
`
`
export CLUSTERDB=/Users/swat/dev/cdb
export CLUSTERDB_HOST=localhost
export CLUSTERDB_PORT=5555
export CLUSTERDB_UPDATABLE=0
` 


Set CLUSTERDB_UPDATABLE to '1' if you always want DB updates allowed.

`export CLUSTERDB_UPDATABLE=1`

Or this to never allow any updates to the database:

`export CLUSTERDB_UPDATABLE=0`

Or leave it undefined if you want to control updatability from the command line.

Now you're ready to put the app in development mode and start it up.

`bin/start`
