
# This is separate from app.py so unit tests can provide an alternate config.
import os
from cluster.app import create_app

create_app()
