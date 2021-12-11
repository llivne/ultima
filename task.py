import controller
from celery import Celery
from persist import PersistUploader


celery_url = "redis://redis:6379"
app = Celery("task", broker=celery_url)
persist = PersistUploader()
controller = controller.MockedUploaderController()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls perform_upload() every 30 seconds
    sender.add_periodic_task(10.0, perform_periodic_upload.s(), expires=30)


@app.task
def perform_periodic_upload():
    items = persist.load_items()
    uploaded_items = []
    for item in items:
        src = item["Source_folder"]
        dest = item["Destination_bucket"]
        item_tuple = (src, dest)
        if item_tuple not in uploaded_items:
            controller.upload_item(item, "celery")
            uploaded_items.append(item_tuple)
        else:
            print(f"{item_tuple} already uploaded in this interval")
