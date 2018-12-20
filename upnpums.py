#!/usr/bin/env python
"""
This code is based off the Miranda.
Christian Lachapelle & Jason Major
19/12/2018
"""
################################
# Interactive UPNP application #
# Craig Heffner                #
# 07/16/2008                   #
################################

import sys

from network.upnp import *
from shell.commandmanager import *

__VERSION__ = "0.1"


# Main
def main(argc, argv):

    # Initilize the shell class
    sh = CmdManager()
    sh.start(argc, argv, interface=sh)

    # Initialize upnp class
    # hp = Upnp(False, False, None, appCommands);


if __name__ == "__main__":
    try:
        print('')
        print('UPnPUMS v%s' % __VERSION__)
        print('The interactive UPnP Universal Media Server')
        print('Christian Lachapelle & Jason Major')
        print('')
        main(len(sys.argv), sys.argv)

    except Exception as e:
        print('Caught main exception:', e)
        sys.exit(1)
