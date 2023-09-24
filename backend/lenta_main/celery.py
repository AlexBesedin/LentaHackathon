from datetime import timedelta

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
    'import-stores-data': {
        'task': 'tasks.import_stores_data',
        'schedule': timedelta(days=1),
    },
}
