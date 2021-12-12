import controller
import configparser
from celery import Celery
from persist import PersistUploader

celery_url = "redis://redis:6379"
app = Celery("task", broker=celery_url)
persist = PersistUploader()

# Load configurations
config = configparser.ConfigParser()
config.read("config.ini")
interval = int(config['periodic']['interval'])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls perform_periodic_upload() every xx seconds
    sender.add_periodic_task(interval, perform_periodic_upload.s())


@app.task
def perform_periodic_upload():
    persist.upload_items()
