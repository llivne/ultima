import controller
import pickle
import os

class PersistUploader:
    def __init__(self, picklefile=os.path.join("persist_data", "persist_picklefile")):
        self.filename = picklefile
        self.controller = controller.MockedUploaderController()

    def add_new_item(self, item):
        with open(self.filename, "ab") as fp:
            pickle.dump(item, fp)

    def load_items(self):
        data = []
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as fr:
                try:
                    while True:
                        data.append(pickle.load(fr))
                except EOFError:
                    pass

        return data

    def upload_items(self):
        items = self.load_items()
        print(f"{len(items)} items were set to be monitored for uploading."
              f" checking if items were modified and updating if required.")

        uploaded_items = []
        for item in items:
            src = item["Source_folder"]
            dest = item["Destination_bucket"]
            regex = item["Regex"]
            item_tuple = (src, dest, regex)
            if item_tuple not in uploaded_items:
                self.controller.upload_item(item, "celery")
                uploaded_items.append(item_tuple)
            else:
                print(f"{item_tuple} already uploaded in this interval")
