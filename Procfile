web: gunicorn school_management.wsgi --log-file -
release: python manage.py migrate_schemas
celery: celery -A school_management worker -l INFO
celery-beat: celery -A school_management beat -l INFO
