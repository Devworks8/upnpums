"""
UPnP Universal Media Server main entry point.
"""

import logging
from pyupnp.logr import Logr
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP

from interfaces import network
from interfaces.pluginmanager import PluginManager
from interfaces.devices import mediaserver

___VERSION___ = (0, 0, 1)

if __name__ == "__main__":
    Logr.configure(logging.DEBUG)

    device = mediaserver.MediaServerDevice()

    upnp = UPnP(device)
    ssdp = SSDP(device)

    upnp.listen()
    ssdp.listen()

    manager = PluginManager()
    _ = network.Daemonize()
