from queue import Queue
import threading
import controller


controller = controller.UploaderController()


class UploaderWorkers (threading.Thread):
    queueLock = threading.Lock()
    workQueue = Queue()
    condition = threading.Event()

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            self.condition.wait()
            self.queueLock.acquire()
            if not self.workQueue.empty():
                item = self.workQueue.get()
                self.queueLock.release()
                controller.do_upload(item, self.name)
            else:
                self.condition.clear()
                self.queueLock.release()


    @classmethod
    def add(cls, item):
        cls.queueLock.acquire()
        print("Adding")
        cls.workQueue.put(item)
        cls.queueLock.release()
        cls.condition.set()


def init_workers():
    thread_list = ["Thread1", "Thread2", "Thread3"]

    threads = []

    # Create new threads
    for t in thread_list:
        thread = UploaderWorkers(t)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    return threads


