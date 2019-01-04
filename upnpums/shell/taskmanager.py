import threading
import _thread
import queue


class TaskManager:
    def __init__(self):
        self.threadID = 1
        self.threadName = ""
        self.object = object
        self.threads = []
        self.threadLock = threading.Lock()
        self.workQueue = queue.Queue(10)
        self.exitFlag = False

    def process_obj(self, threadName, workQueue, object):
        while not self.exitFlag:
            self.threadLock.acquire()

            if not workQueue.empty():
                self.threadLock.release()
                eval(object)
            else:
                self.threadLock.release()

    def add_thread(self, threadName, object):
        try:
            _thread.start_new_thread(object, (threadName))
        except:
            print("Error: unable to start thread")

        self.threads.append(thread)
        self.threadID += 1

    def terminate(self, threadName):
        threadName.exit()
