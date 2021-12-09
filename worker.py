from queue import Queue
import threading
import controller
import configparser


class UploaderWorkers (threading.Thread):
    queueLock = threading.Lock()
    workQueue = Queue()
    condition = threading.Event()

    def __init__(self, worker_id):
        threading.Thread.__init__(self)
        self.worker_id = worker_id
        self.controller = controller.MockedUploaderController()

    def run(self):
        while True:
            self.condition.wait()
            self.queueLock.acquire()
            if not self.workQueue.empty():
                item = self.workQueue.get()
                self.queueLock.release()
                self.controller.upload_item(item, self.worker_id)
            else:
                self.condition.clear()
                self.queueLock.release()


    @classmethod
    def add(cls, item):
        cls.queueLock.acquire()
        print(f"Adding {item}")
        cls.workQueue.put(item)
        cls.queueLock.release()
        cls.condition.set()


def init_workers():
    threads = []

    # Load worker configurations
    config = configparser.ConfigParser()
    config.read("config.ini")
    num_of_workers = int(config['workers']['num_of_workers'])

    # Create new threads
    for i in range(num_of_workers):
        thread = UploaderWorkers(f"worker-{i+1}")
        thread.daemon = True
        thread.start()
        threads.append(thread)

    return threads


