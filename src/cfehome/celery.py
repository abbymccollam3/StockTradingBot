from celery import Celery

app = Celery("cfehome")
app.config_from_object(
    'django.conf:settings', 
    namespace='CELERY'
)
app.autodiscover_tasks() #looks for tasks.py