"""
Universal Multimedia Server
"""

from pyaudio import *
from pyAudioAnalysis import *
from twisted import *


class Audio:
    def __init__(self):
        pass


class Ums:
    ip = False
    port = False
    completer = False
    DEFAULT_IP = "239.255.255.250"
    DEFAULT_PORT = 1900
    UPNP_VERSION = '1.0'
    MAX_RECV = 8192
    MAX_HOSTS = 10
    TIMEOUT = 200
    HTTP_HEADERS = []
    ENUM_HOSTS = {}
    VERBOSE = True
    UNIQ = False
    DEBUG = True
    LOG_FILE = False
    BATCH_FILE = None
    IFACE = None
    STARS = '****************************************************************'

    def __init__(self):
        pass

    def start(self):
        print("started")

    def stop(self):
        print("stopped")
