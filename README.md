# clusterDb
RestAPI for single cell clusters.

### Install

You will need to have Python3.7 and Git installed on your machine.

First clone the repo somewhere on your disk.

`cd /path/to/my/workspace/`

`git clone https://github.com/terraswat/clusterDb`

`cd clusterDb`


Create a virtual environment and install the requirements.

``virtualenv -p `which python3.7` venv``

`cd clusterDb`

`source ../venv/bin/activate`

`pip install -r requirements.txt`

Set up env vars where CLUSTERDB_UPDATABLE should only be set to '1' if you always want
DB updates allowed. Leave it undefined if you want to control updatability with this env var
on the command line.

`deactivate`

`vi ../venv/bin/activate`

Add the following lines to the bottom of the file:

`
export CLUSTERDB=</path/to/my/workspace/>
export CLUSTERDB_HOST=<hostname>
export CLUSTERDB_PORT=<port>
`

Define this before starting to allow database updates by anyone:

`export CLUSTERDB_UPDATABLE=1`

Or this to not allow any updates to the database:

`export CLUSTERDB_UPDATABLE=0`

Now you're ready to put the app in development mode and start it up.

`bin/start`
