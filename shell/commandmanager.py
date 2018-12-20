from shell.commands.common import *
from shell.commands.upnp import *


# Most of the CmdCompleter class was originally written by John Kenyan
# It serves to tab-complete commands inside the program's shell
class CmdCompleter:
    def __init__(self, commands):
        self.commands = commands

    # Traverses the list of available commands
    def traverse(self, tokens, tree):
        retVal = []

        # If there are no commands, or no user input, return null
        if tree is None or len(tokens) == 0:
            retVal = []

        # If there is only one word, only auto-complete the primary commands
        elif len(tokens) == 1:
            retVal = [x + ' ' for x in tree if x.startswith(tokens[0])]

        # Else auto-complete for the sub-commands
        elif tokens[0] in tree.keys():
            retVal = self.traverse(tokens[1:], tree[tokens[0]])

        return retVal

    # Returns a list of possible commands that match the partial command that the user has entered
    def complete(self, text, state):
        try:
            tokens = readline.get_line_buffer().split()

            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append('')
            results = self.traverse(tokens, self.commands) + [None]
            return results[state]

        except Exception as e:
            print("Failed to complete command: %s" % str(e))

        return


class CmdManager(CmdCompleter):
    def __init__(self, argc, argv):
        self.action = False
        self.funPtr = False
        self.BATCH_FILE = None
        # Table of valid commands - all primary commands must have an associated function
        self.appCommands = {
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
        super().__init__(self.appCommands)
        self.cmdline()
        self.setauto()
        # Check command line options
        self.parseCliOpts(argc, argv)

    def cmdline(self):
        # Set up tab completion and command history
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    # Check command line options
    def parseCliOpts(argc, argv, hp=None):
        try:
            opts, args = getopt.getopt(argv[1:], 's:l:i:b:udvh')

        except getopt.GetoptError as e:
            print('Usage Error:', e)
            usage()

        else:
            for (opt, arg) in opts:

                if opt == '-s':
                    print('')
                    load(2, ['load', arg], hp)
                    print('')

                elif opt == '-l':
                    print('')
                    log(2, ['log', arg], hp)
                    print('')

                elif opt == '-u':
                    hp.UNIQ = toggleVal(hp.UNIQ)

                elif opt == '-d':
                    hp.DEBUG = toggleVal(hp.DEBUG)
                    print('Debug mode enabled!')

                elif opt == '-v':
                    hp.VERBOSE = toggleVal(hp.VERBOSE)
                    print('Verbose mode enabled!')

                elif opt == '-b':
                    hp.BATCH_FILE = open(arg, 'r')
                    print("Processing commands from '%s'..." % arg)

                elif opt == '-h':
                    usage()

                elif opt == '-i':
                    networkInterfaces = []
                    requestedInterface = arg
                    interfaceName = None
                    found = False

                    # Get a list of network interfaces. This only works on unix boxes.
                    try:
                        if platform.system() != 'Windows':
                            fp = open('/proc/net/dev', 'r')

                            for line in fp.readlines():

                                if ':' in line:
                                    interfaceName = line.split(':')[0].strip()

                                    if interfaceName == requestedInterface:
                                        found = True
                                        break

                                    else:
                                        networkInterfaces.append(line.split(':')[0].strip())
                            fp.close()

                        else:
                            networkInterfaces.append('Run ipconfig to get a list of available network interfaces!')

                    except Exception as e:
                        print('Error opening file:', e)
                        print("If you aren't running Linux, this file may not exist!")

                    if not found and len(networkInterfaces) > 0:
                        print("Failed to find interface '%s'; try one of these:\n" % requestedInterface)

                        for iface in networkInterfaces:
                            print(iface)

                        print('')
                        sys.exit(1)

                    else:
                        if not hp or not hp.initSockets(False, False, interfaceName):
                            print(
                                'Binding to interface %s failed; are you sure you have root privilages??' % interfaceName)

    def setauto(self):
        # The load command should auto complete on the contents of the current directory
        for file in os.listdir(os.getcwd()):
            self.appCommands['load'][file] = None
