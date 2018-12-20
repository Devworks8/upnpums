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

from shell.helpers import *
from network.upnp import *
from shell.commandmanager import *

__VERSION__ = "0.1"


# Main
def main(argc, argv):

    # Initilize the shell class
    sh = CmdManager(argc, argv)

    # Initialize upnp class
    # hp = Upnp(False, False, None, appCommands);

    # Set some default values
    # hp.UNIQ = True
    #hp.VERBOSE = False

    # Main loop
    while True:
        # Drop user into shell
        if sh.BATCH_FILE is not None:
            (argc, argv) = getFileInput(sh)

        else:
            (argc, argv) = getUserInput(sh, False)

        if argc == 0:
            continue

        sh.action = argv[0]
        sh.funcPtr = False

        print('')

        # Parse actions
        try:
            if sh.action in sh.appCommands:
                sh.funcPtr = eval(sh.action)

        except:
            sh.funcPtr = False
            sh.action = False

        if callable(sh.funcPtr):
            if argc == 2 and argv[1] == 'help':
                showHelp(argv[0])

            else:
                try:
                    sh.funcPtr(argc, argv, sh)

                except KeyboardInterrupt:
                    print('\nAction interrupted by user...')
            print('')
            continue

        print('Invalid command. Valid commands are:')
        print('')
        showHelp(False)
        print('')


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
