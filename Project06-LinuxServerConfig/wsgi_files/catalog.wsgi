# /var/www/catalog/catalog.conf

# flask-dance 
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# add your python files to the python path, that is needed to find the app.py file (where your flask app is located)
import sys
sys.path.insert(0, '/var/www/catalog')

# tell the application where the root is, it is required for loading templates.
from application import app as application
application.root_path = '/var/www/catalog'

