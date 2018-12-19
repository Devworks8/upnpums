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

from shell.commands.common import *
from shell.helpers import *
from network.upnp import *
from shell.commandmanager import *

__VERSION__ = 0.1


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

    # Initilize the shell class
    sh = CmdManager(appCommands)

    # Initialize upnp class
    # hp = Upnp(False, False, None, appCommands);

    # Set up tab completion and command history
    readline.parse_and_bind("tab: complete")
    readline.set_completer(sh.complete)

    # Set some default values
    # hp.UNIQ = True
    #hp.VERBOSE = False


    # Check command line options
    parseCliOpts(argc, argv, sh)

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
            if sh.action in appCommands:
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
        print('UPnPUMS v%' % __VERSION__)
        print('The interactive UPnP Universal Media Server')
        print('Christian Lachapelle & Jason Major')
        print('')
        main(len(sys.argv), sys.argv)

    except Exception as e:
        print('Caught main exception:', e)
        sys.exit(1)
