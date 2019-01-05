import os

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


# TODO: Complete error handling.
class CmdManager(CmdCompleter):
    def __init__(self, config, db):
        self._db = db
        self._config = config
        self.action = False
        self.funPtr = False
        self.BATCH_FILE = None
        self.LOG_FILE = False
        self.UNIQ = True
        self.VERBOSE = False
        # Table of valid commands - all primary commands must have an associated function
        self.appCommands = {**commonCommands, **upnpCommands}
        self.activeInterface = []
        super().__init__(self.appCommands)
        self.__cmdline()
        self.__setauto()

    def __cmdline(self):
        """
        Set up tab completion and command history
        :return:
        """
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    def __parseCliOpts(self, argc, argv, interface):
        """
        Check command line options.
        :param argc: Argument count
        :param argv: Argument list
        :param interface: Network interface
        :return:
        """
        try:
            opts, args = getopt.getopt(argv[1:], 's:l:i:b:udvh')

        except getopt.GetoptError as e:
            print('Usage Error:', e)
            usage()

        else:
            for (opt, arg) in opts:

                if opt == '-s':
                    print('')
                    load(2, ['load', arg], interface)
                    print('')

                elif opt == '-l':
                    print('')
                    log(2, ['log', arg], interface)
                    print('')

                elif opt == '-u':
                    interface.UNIQ = toggleVal(interface.UNIQ)

                elif opt == '-d':
                    interface.DEBUG = toggleVal(interface.DEBUG)
                    print('Debug mode enabled!')

                elif opt == '-v':
                    interface.VERBOSE = toggleVal(interface.VERBOSE)
                    print('Verbose mode enabled!')

                elif opt == '-b':
                    interface.BATCH_FILE = open(arg, 'r')
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
                        if isinstance(interface, CmdManager) or not interface.initSockets(False, False, interfaceName):
                            print(
                                'Binding to interface %s failed; are you sure you have root privilages??' % interfaceName)

    def __setauto(self):
        """
        The load command should auto complete on the contents of the current directory.
        :return:
        """
        for file in os.listdir(os.getcwd()):
            self.appCommands['load'][file] = None

    def start(self, argc, argv, interface, config, db, taskmanager):
        """
        Start the shell interface.
        :param argc: Argument count
        :param argv: Argument list
        :param interface: Shell object
        :param config: Config object
        :param db: Database object
        :param taskmanager: Task Manager object
        :return:
        """

        # Check command line options
        self.__parseCliOpts(argc, argv, interface)

        # Main loop
        while True:

            # FIXME: Need to clean up stopped tasks.
            """
            # Remove stopped threads.
            print(taskmanager.threads.items())
            for k, v in taskmanager.threads.items():
                
                if 'stopped' in v:
                    taskmanager.stop(k)
            """

            # Drop user into shell
            if interface.BATCH_FILE is not None:
                (argc, argv) = getFileInput(interface)

            else:
                (argc, argv) = getUserInput(interface, False)

            if argc == 0:
                continue

            interface.action = argv[0]
            interface.funcPtr = False

            print('')

            # Parse actions
            try:
                if interface.action in interface.appCommands:
                    interface.funcPtr = eval(interface.action)

            except:
                interface.funcPtr = False
                interface.action = False

            if callable(interface.funcPtr):
                if argc == 2 and argv[1] == 'help':
                    showHelp(argv[0])

                else:
                    try:
                        interface.funcPtr(argc, argv, interface, config, db)

                    except KeyboardInterrupt:
                        print('\nAction interrupted by user...')
                print('')
                continue

            print('Invalid command. Valid commands are:')
            print('')
            showHelp(False)
            print('')
