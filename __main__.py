"""
UPnP Universal Media Server main entry point.
"""

from Interfaces import Network

__AUTHOR__ = "Christian Lachapelle"
___VERSION___ = (0, 0, 1)

if __name__ == "__main__":
    _ = Network.Daemonize()
