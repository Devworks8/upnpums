"""
Network.py is part of the Interfaces package.
"""

import interfaces.devices.mediaserver as media


class Daemonize(media.MediaServerDevice):
    """
    All server work done here.
    """
    def __init__(self):
        super().__init__()
