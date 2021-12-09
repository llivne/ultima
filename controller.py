from time import sleep


class UploaderController:
    def __init__(self):
        pass

    def do_upload(self, item, thread_name):
        print(f"uploading {item} with {thread_name}")
        sleep(20)
        print(f"done_uploading with {thread_name}")
