web: bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT django_project/settings.py
worker: bin/python django_project/manage.py celeryd -E -B --loglevel=INFO
