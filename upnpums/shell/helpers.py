################ End Action Functions ######################

import sys
import platform
import getopt
import readline


def showHelp(command):
    """
    Show command help.
    :param command: Command name
    :return: String
    """
    # Detailed help info for each command
    helpInfo = {
        'help': {
            'longListing':
                'Description:\n' \
                '\tLists available commands and command descriptions\n\n' \
                'Usage:\n' \
                '\t%s\n' \
                '\t<command> help',
            'quickView':
                'Show program help'
        },
        'quit': {
            'longListing':
                'Description:\n' \
                '\tQuits the interactive shell\n\n' \
                'Usage:\n' \
                '\t%s',
            'quickView':
                'Exit this shell'
        },
        'exit': {

            'longListing':
                'Description:\n' \
                '\tExits the interactive shell\n\n' \
                'Usage:\n' \
                '\t%s',
            'quickView':
                'Exit this shell'
        },
        'save': {
            'longListing':
                'Description:\n' \
                '\tSaves current config/host information to disk.\n\n' \
                'Usage:\n' \
                '\t%s <config | <data | info <host#>> [file prefix]>\n' \
                "\tSpecifying 'data' will save the raw host data to a file suitable for importing later via 'load'\n" \
                "\tSpecifying 'info' will save data for the specified host in a human-readable format\n" \
                "\tSpecifying 'config' will save the current configuration to file\n" \
                "\tSpecifying a file prefix will save files in for format of 'struct_[prefix].mir' and info_[prefix].mir\n\n" \
                'Example:\n' \
                '\t> save data wrt54g\n' \
                '\t> save info 0 wrt54g\n' \
                '\t> save config\n\n' \
                'Notes:\n' \
                "\to Data files are saved as 'struct_[prefix].mir'; info files are saved as 'info_[prefix].mir.'\n" \
                "\to Config files are saved as 'YAML struct [settings].yml.'\n" \
                "\to If no prefix is specified, the host index number will be used for the prefix.\n" \
                "\to The data saved by the 'save info' command is the same as the output of the 'host details' command.",
            'quickView':
                'Save current config/host data to file'
        },
        'set': {
            'longListing':
                'Description:\n' \
                '\tAllows you  to view and edit application settings.\n\n' \
                'Usage:\n' \
                '\t%s <show | <config setting> | uniq | debug | verbose | version <version #> | iface <interface> | socket <ip:port> | timeout <seconds> | max <count> >\n' \
                "\t'show' displays the current program settings\n" \
                "\t'uniq' toggles the show-only-uniq-hosts setting when discovering UPNP devices\n" \
                "\t'debug' toggles debug mode\n" \
                "\t'verbose' toggles verbose mode\n" \
                "\t'version' changes the UPNP version used\n" \
                "\t'iface' changes the network interface in use\n" \
                "\t'socket' re-sets the multicast IP address and port number used for UPNP discovery\n" \
                "\t'timeout' sets the receive timeout period for the msearch and pcap commands (default: infinite)\n" \
                "\t'max' sets the maximum number of hosts to locate during msearch and pcap discovery modes\n" \
                "\t'<config setting>' change a config setting\n\n" \
                'Example:\n' \
                '\t> set socket 239.255.255.250:1900\n' \
                '\t> set uniq\n' \
                '\t> set interface_ums_ip 255.255.255.255\n\n'
                'Notes:\n' \
                "\tIf given no options, 'set' will display help options",
            'quickView':
                'Show/define application settings'
        },
        'head': {
            'longListing':
                'Description:\n' \
                '\tAllows you to view, set, add and delete the SSDP header values used in SSDP transactions\n\n' \
                'Usage:\n' \
                '\t%s <show | del <header> | set <header>  <value>>\n' \
                "\t'set' allows you to set SSDP headers used when sending M-SEARCH queries with the 'msearch' command\n" \
                "\t'del' deletes a current header from the list\n" \
                "\t'show' displays all current header info\n\n" \
                'Example:\n' \
                '\t> head show\n' \
                '\t> head set MX 3',
            'quickView':
                'Show/define SSDP headers'
        },
        'host': {
            'longListing':
                'Description:\n' \
                "\tAllows you to query host information and iteract with a host's actions/services.\n\n" \
                'Usage:\n' \
                '\t%s <list | get | info | summary | details | send> [host index #]\n' \
                "\t'list' displays an index of all known UPNP hosts along with their respective index numbers\n" \
                "\t'get' gets detailed information about the specified host\n" \
                "\t'details' gets and displays detailed information about the specified host\n" \
                "\t'summary' displays a short summary describing the specified host\n" \
                "\t'info' allows you to enumerate all elements of the hosts object\n" \
                "\t'send' allows you to send SOAP requests to devices and services *\n\n" \
                'Example:\n' \
                '\t> host list\n' \
                '\t> host get 0\n' \
                '\t> host summary 0\n' \
                '\t> host info 0 deviceList\n' \
                '\t> host send 0 <device name> <service name> <action name>\n\n' \
                'Notes:\n' \
                "\to All host commands support full tab completion of enumerated arguments\n" \
                "\to All host commands EXCEPT for the 'host send', 'host info' and 'host list' commands take only one argument: the host index number.\n" \
                "\to The host index number can be obtained by running 'host list', which takes no futher arguments.\n" \
                "\to The 'host send' command requires that you also specify the host's device name, service name, and action name that you wish to send,\n\t  in that order (see the last example in the Example section of this output). This information can be obtained by viewing the\n\t  'host details' listing, or by querying the host information via the 'host info' command.\n" \
                "\to The 'host info' command allows you to selectively enumerate the host information data structure. All data elements and their\n\t  corresponding values are displayed; a value of '{}' indicates that the element is a sub-structure that can be further enumerated\n\t  (see the 'host info' example in the Example section of this output).",
            'quickView':
                'View and send host list and host information'
        },
        'pcap': {
            'longListing':
                'Description:\n' \
                '\tPassively listens for SSDP NOTIFY messages from UPNP devices\n\n' \
                'Usage:\n' \
                '\t%s',
            'quickView':
                'Passively listen for UPNP hosts'
        },
        'msearch': {
            'longListing':
                'Description:\n' \
                '\tActively searches for UPNP hosts using M-SEARCH queries\n\n' \
                'Usage:\n' \
                "\t%s [device | service] [<device name> | <service name>]\n" \
                "\tIf no arguments are specified, 'msearch' searches for upnp:rootdevices\n" \
                "\tSpecific device/services types can be searched for using the 'device' or 'service' arguments\n\n" \
                'Example:\n' \
                '\t> msearch\n' \
                '\t> msearch service WANIPConnection\n' \
                '\t> msearch device InternetGatewayDevice',
            'quickView':
                'Actively locate UPNP hosts'
        },
        'load': {
            'longListing':
                'Description:\n' \
                "\tLoads host data from a struct file previously saved with the 'save data' command\n\n" \
                'Usage:\n' \
                '\t%s <file name>',
            'quickView':
                'Restore previous host data from file'
        },
        'log': {
            'longListing':
                'Description:\n' \
                '\tLogs user-supplied commands to a log file\n\n' \
                'Usage:\n' \
                '\t%s <log file name>',
            'quickView':
                'Logs user-supplied commands to a log file'
        }
    }

    try:
        print(helpInfo[command]['longListing'] % command)

    except:
        for command, cmdHelp in helpInfo.items():
            print("%s\t\t%s" % (command, cmdHelp['quickView']))


def usage():
    """
    Display usage
    :return: String
    """
    print('''
Command line usage: %s [OPTIONS]

	-s <struct file>	Load previous host data from struct file
	-l <log file>		Log user-supplied commands to log file
	-d			Enable debug mode
	-v			Enable verbose mode
	-h 			Show help
''' % sys.argv[0])
    sys.exit(1)


def toggleVal(val):
    """
    Toggle boolean values
    :param val: Boolean
    :return: Boolean
    """
    if val:
        return False

    else:
        return True


def getUserInput(hp, shellPrompt):
    """
    Prompt for user input
    :param hp: Shell object
    :param shellPrompt: Displayed prompt
    :return:
    """
    defaultShellPrompt = 'upnp> '

    if hp.BATCH_FILE is not None:
        return getFileInput(hp)

    if not shellPrompt:
        shellPrompt = defaultShellPrompt

    try:
        uInput = input(shellPrompt).strip()
        argv = uInput.split()
        argc = len(argv)

    except KeyboardInterrupt as e:
        print('\n')

        if shellPrompt == defaultShellPrompt:
            quit(0, [], hp)

        return 0, None

    if hp.LOG_FILE:
        try:
            hp.LOG_FILE.write("%s\n" % uInput)

        except:
            print('Failed to log data to log file!')

    return argc, argv


def getFileInput(object):
    """
    Read scripted commands from a file.
    :param object: File object
    :return:
    """
    data = False
    line = object.BATCH_FILE.readline()

    if line:
        data = True
        line = line.strip()

    argv = line.split()
    argc = len(argv)

    if not data:
        object.BATCH_FILE.close()
        object.BATCH_FILE = None

    return argc, argv


def cleanup(interface):
    """
    Close the log file if open.
    :param interface: Shell object
    :return:
    """
    if interface.LOG_FILE:
        interface.LOG_FILE.close()


def notImplemented(command) -> None:
    print("INFO: {command} not implemented.".format(command=command))
    return
