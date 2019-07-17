# clusterDb
RestAPI for single cell clusters.

### Install

You will need to have Python3.7 and Git installed on your machine.

Define an environment variable to be the root of your install.

`export CLUSTERDB=/some-path`

Clone the repository.

`cd $CLUSTERDB`

`git clone https://github.com/stuartlab-UCSC/cluster-db`


Create a virtual environment and install the requirements.

``virtualenv -p `which python3.7` env``

`cd clusterDb`

`source ../env/bin/activate`

`pip install -r requirements.txt`

`deactivate`


Now add a configuration file at `$CLUSTERDB/clusterDbConfig.sh`, something like the 
below:

Production running in background:
```
export BACKGROUND=1
export HOST=localhost
export PORT=9000
export HTTPS=1
export VIEWER_URL=https://cellatlas.ucsc.edu/
export WWW_SOCKET=127.0.0.1:$PORT
source /<protected-dir>/clusterDbSecret
source $CLUSTERDB/env/bin/activate
```

or using the localhost in a dev environment running in foreground:
```
export FLASK_DEBUG=True
export FLASK_ENV=development
export HOST=localhost
export PORT=5555
export VIEWER_URL=http://localhost:3000/
export WWW_SOCKET=127.0.0.1:$PORT
source $CLUSTERDB/env/bin/activate
```

Now you're ready to start the app.

`bin/start`

Logins: to use the authentication and authorization functions, a secret string must be 
accessible in the application. One way to do this is to put the string in a protected directory
and source that file from your configuration file.

