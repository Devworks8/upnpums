#!/usr/bin/env python
################################
# Interactive UPNP application #
# Craig Heffner                #
# 07/16/2008                   #
################################

import sys
import os

from shell.commands import *
from shell.helpers import *
from network.upnp import *


# Main
def main(argc, argv):
    # Table of valid commands - all primary commands must have an associated function
    appCommands = {
        'help': {
            'help': None
        },
        'quit': {
            'help': None
        },
        'exit': {
            'help': None
        },
        'save': {
            'data': None,
            'info': None,
            'help': None
        },
        'load': {
            'help': None
        },
        'set': {
            'uniq': None,
            'socket': None,
            'show': None,
            'iface': None,
            'debug': None,
            'version': None,
            'verbose': None,
            'timeout': None,
            'max': None,
            'help': None
        },
        'head': {
            'set': None,
            'show': None,
            'del': None,
            'help': None
        },
        'host': {
            'list': None,
            'info': None,
            'get': None,
            'details': None,
            'send': None,
            'summary': None,
            'help': None
        },
        'pcap': {
            'help': None
        },
        'msearch': {
            'device': None,
            'service': None,
            'help': None
        },
        'log': {
            'help': None
        },
        'debug': {
            'command': None,
            'help': None
        }
    }

    # The load command should auto complete on the contents of the current directory
    for file in os.listdir(os.getcwd()):
        appCommands['load'][file] = None

    # Initialize upnp class
    hp = Upnp(False, False, None, appCommands);

    # Set up tab completion and command history
    readline.parse_and_bind("tab: complete")
    readline.set_completer(hp.completer.complete)

    # Set some default values
    hp.UNIQ = True
    hp.VERBOSE = False
    action = False
    funPtr = False

    # Check command line options
    parseCliOpts(argc, argv, hp)

    # Main loop
    while True:
        # Drop user into shell
        if hp.BATCH_FILE is not None:
            (argc, argv) = getFileInput(hp)
        else:
            (argc, argv) = getUserInput(hp, False)
        if argc == 0:
            continue
        action = argv[0]
        funcPtr = False

        print('')
        # Parse actions
        try:
            if action in appCommands:
                funcPtr = eval(action)
        except:
            funcPtr = False
            action = False

        if callable(funcPtr):
            if argc == 2 and argv[1] == 'help':
                showHelp(argv[0])
            else:
                try:
                    funcPtr(argc, argv, hp)
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
        print('Miranda v1.3')
        print('The interactive UPnP client')
        print('Craig Heffner, http://www.devttys0.com')
        print('')
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print('Caught main exception:', e)
        sys.exit(1)
