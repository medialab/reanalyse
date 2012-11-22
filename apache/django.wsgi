import os
import sys

##### PROD
sys.path.append('/var/opt/reanalyse')
sys.path.append('/var/opt')

os.environ['DJANGO_SETTINGS_MODULE'] = 'reanalyse.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
