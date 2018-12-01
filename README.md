# clusterDb
RestAPI for single cell clusters.

### Install

You will need to have installed:
    Python with [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
    [Git](https://git-scm.com/) installed on your machine.

First clone the repo somewhere on your disk.

`cd /path/to/my/workspace/`

`git clone https://github.com/Stuartlab-UCSC/clusterDb`

`cd clusterDb`

Create a virtual environment, fire it up, and install the requirements.

``virtualenv -p `which python3` venv``

`source venv/bin/activate`

`pip install -r requirements.txt`

Now you're ready to put the app in development mode and start it up.

`python setup.py develop`

`python cluster/app.py`