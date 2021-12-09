
import threading
from queue import Queue

from controller import UploaderController

uploader_q = Queue()

controller = UploaderController()


class ConsumerThread(threading.Thread):

    def __init__(self):
        super(ConsumerThread, self).__init__()
        self.condition = threading.Condition()

    def run(self):
        with self.condition:
            while True:
                while not uploader_q.empty():
                    item = uploader_q.get()
                    controller.do_upload(item)
                self.condition.wait()

    def add(self, item):
        with self.condition:
            print("adding")
            uploader_q.put(item)
            self.condition.notifyAll()


