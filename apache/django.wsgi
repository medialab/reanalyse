import os
import sys

##### PROD
#sys.path.append('/mnt/expand/reanalyse')
#sys.path.append('/mnt/expand')

##### DEV
sys.path.append('/home/pj/djangos/reanalyse')
sys.path.append('/home/pj/djangos')

os.environ['DJANGO_SETTINGS_MODULE'] = 'reanalyse.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
