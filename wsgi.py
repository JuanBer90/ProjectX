import os
import sys
from unipath import Path
p = Path(__file__)
sys.path = [p.ancestor(1)] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_produccion'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()