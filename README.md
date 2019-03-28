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

Add configuration environment variables to the bottom of the file, something like:
`
export CLUSTERDB=/data/cdb
export HOST=hexcalc.ucsc.edu
export PORT=9000
export WWW_SOCKET=127.0.0.1:$PORT
`
or this:
`
export CLUSTERDB=/Users/swat/dev/cdb
export HOST=localhost
export PORT=5555
export WWW_SOCKET=127.0.0.1:$PORT
` 
If you want to use https, also add environment variables something like:
`
export HTTPS=1
export CERTS=/data/certs
export CERT=$CERTS/server.crt
export CA=$CERTS/chain.crt
export KEY=$CERTS/server.key
`

Set CLUSTERDB_UPDATABLE to '1' if you always want DB updates allowed.

`export CLUSTERDB_UPDATABLE=1`

Or this to never allow any updates to the database:

`export CLUSTERDB_UPDATABLE=0`

Now you're ready to put the app in development mode and start it up.

`bin/start`
