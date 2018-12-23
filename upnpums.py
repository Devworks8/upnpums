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

from config.configure import *
from database.dbparser import *
from shell.commandmanager import *

__VERSION__ = "0.1"


# Main
def main(argc, argv):
    # Initialize the config
    cm = CfgManager()
    dm = DbParser(config=cm)
    print(cm.get('database_path')[0][1])
    dm.list_files(cm.get('database_library')[0][1])

    # Initilize the shell class
    sh = CmdManager(config=cm)
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
