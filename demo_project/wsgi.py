import os
import sys

sys.path.append('/home/juanber/PycharmProjects/ProjectX')
	#carpeta donde está el proyecto clonado.
sys.path.append('/home/juanber/PycharmProjects/ProjectX/demo_project')
	#carpeta que contiene a wsgi.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")
	#se setea al settings de nuestro proyecto

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()




