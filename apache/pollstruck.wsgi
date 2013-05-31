import os, sys

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

#Add the path to 3rd party django application to django itself.
sys.path.append('/srv/pollstruck/pollster')
sys.path.append('/srv/pollstruck/pollster/lib')
#sys.path.insert(0, '/srv/squash/venv/lib/python2.6/site-packages/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pollster.settings'

os.environ['PYTHON_EGG_CACHE'] = '/srv/pollstruck/egg_cache'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
