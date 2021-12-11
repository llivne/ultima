import controller
from celery import Celery
from persist import PersistUploader


celery_url = "redis://redis:6379"
app = Celery("task", broker=celery_url)
persist = PersistUploader()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls perform_upload() every 30 seconds
    sender.add_periodic_task(10.0, perform_periodic_upload.s(), expires=30)


@app.task
def perform_periodic_upload():
    persist.upload_items()
