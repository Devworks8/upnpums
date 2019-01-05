import multiprocessing as mp
from collections import OrderedDict


class TaskManager:
    def __init__(self):
        self.threads = OrderedDict()

    def add_thread(self, object, arguments):
        """
        Add a new thread to the pool.
        :param object: function to execute
        :param arguments: any parameters the function takes
        :return:
        """
        try:
            thread = mp.Process(target=object, args=arguments)
            self.threads[object.__name__] = thread
        except:
            print("Error: unable to start thread")

    def start(self, threadname=None):
        """
        Start a thread.
        :param threadname: thread to start. None will start them all.
        :return:
        """
        if threadname:
            try:
                self.threads.get(threadname).start()
            except:
                print("Error: {threadname} failed to start.".format(threadname=threadname))
        else:
            for k, v in self.threads:
                try:
                    v.start()
                except:
                    print("Error: {threadname} failed to start.".format(threadname=k))

    def stop(self, threadname):
        """
        Stop a thread.
        :param threadname: thread to start. ALL will stop them all.
        :return:
        """
        if threadname is 'ALL':
            for k, v in self.threads.items():
                try:
                    v.join()
                except:
                    print("Error: {threadname} failed to close.".format(threadname=k))
        else:
            try:
                self.threads[threadname].join()
            except:
                print("Error: {threadname} failed to close.".format(threadname=threadname))

    def cleanup(self):
        self.stop('ALL')
