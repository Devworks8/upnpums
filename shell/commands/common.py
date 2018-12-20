import sys
import os
import pickle
import time
import base64

from network.ums import *
from shell.helpers import *

interfaces = {"ums": "Ums",
              "upnp": "Upnp"}

commonCommands = {
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
    'log': {
        'help': None
    },
    'debug': {
        'command': None,
        'help': None
    },
    'stop': {
        'interface': None
    },
    'start': {
        'interface': None
    }
}


def start(argc, argv, interface):
    if argv[1].lower() in interfaces:
        iface = eval(interfaces[argv[1].lower()] + "()")
        iface.start()


def stop(argc, argv, interface):
    if argv[1].lower() in interfaces:
        iface = eval(interfaces[argv[1].lower()] + "()")
        iface.stop()


# Manipulate application settings
def set(argc, argv, hp):
    if argc >= 2:
        action = argv[1]
        if action == 'uniq':
            hp.UNIQ = toggleVal(hp.UNIQ)
            print("Show unique hosts set to: %s" % hp.UNIQ)
            return
        elif action == 'debug':
            hp.DEBUG = toggleVal(hp.DEBUG)
            print("Debug mode set to: %s" % hp.DEBUG)
            return
        elif action == 'verbose':
            hp.VERBOSE = toggleVal(hp.VERBOSE)
            print("Verbose mode set to: %s" % hp.VERBOSE)
            return
        elif action == 'version':
            if argc == 3:
                hp.UPNP_VERSION = argv[2]
                print('UPNP version set to: %s' % hp.UPNP_VERSION)
            else:
                showHelp(argv[0])
            return
        elif action == 'iface':
            if argc == 3:
                hp.IFACE = argv[2]
                print('Interface set to %s, re-binding sockets...' % hp.IFACE)
                if hp.initSockets(hp.ip, hp.port, hp.IFACE):
                    print('Interface change successful!')
                else:
                    print('Failed to bind new interface - are you sure you have root privilages??')
                    hp.IFACE = None
                return
        elif action == 'socket':
            if argc == 3:
                try:
                    (ip, port) = argv[2].split(':')
                    port = int(port)
                    hp.ip = ip
                    hp.port = port
                    hp.cleanup()
                    if not hp.initSockets(ip, port, hp.IFACE):
                        print("Setting new socket %s:%d failed!" % (ip, port))
                    else:
                        print("Using new socket: %s:%d" % (ip, port))
                except Exception as e:
                    print('Caught exception setting new socket:', e)
                return
        elif action == 'timeout':
            if argc == 3:
                try:
                    hp.TIMEOUT = int(argv[2])
                except Exception as e:
                    print('Caught exception setting new timeout value:', e)
                return
        elif action == 'max':
            if argc == 3:
                try:
                    hp.MAX_HOSTS = int(argv[2])
                except Exception as e:
                    print('Caught exception setting new max host value:', e)
                return
        elif action == 'show':
            print('Multicast IP:          ', hp.ip)
            print('Multicast port:        ', hp.port)
            print('Network interface:     ', hp.IFACE)
            print('Receive timeout:       ', hp.TIMEOUT)
            print('Host discovery limit:  ', hp.MAX_HOSTS)
            print('Number of known hosts: ', len(hp.ENUM_HOSTS))
            print('UPNP version:          ', hp.UPNP_VERSION)
            print('Debug mode:            ', hp.DEBUG)
            print('Verbose mode:          ', hp.VERBOSE)
            print('Show only unique hosts:', hp.UNIQ)
            print('Using log file:        ', hp.LOG_FILE)
            return

    showHelp(argv[0])
    return


# Host command. It's kind of big.
def host(argc, argv, hp):
    hostInfo = None
    indexList = []
    indexError = "Host index out of range. Try the 'host list' command to get a list of known hosts"

    if argc >= 2:
        action = argv[1]
        if action == 'list':
            if len(hp.ENUM_HOSTS) == 0:
                print("No known hosts - try running the 'msearch' or 'pcap' commands")
                return
            for index, hostInfo in hp.ENUM_HOSTS.items():
                print("\t[%d] %s" % (index, hostInfo['name']))
            return
        elif action == 'details':
            if argc == 3:
                try:
                    index = int(argv[2])
                    hostInfo = hp.ENUM_HOSTS[index]
                except Exception as e:
                    print(indexError)
                    return

                try:
                    # If this host data is already complete, just display it
                    if hostInfo['dataComplete']:
                        hp.showCompleteHostInfo(index, False)
                    else:
                        print("Can't show host info because I don't have it. Please run 'host get %d'" % index)
                except KeyboardInterrupt as e:
                    print("")
                    pass
                return

        elif action == 'summary':
            if argc == 3:

                try:
                    index = int(argv[2])
                    hostInfo = hp.ENUM_HOSTS[index]
                except:
                    print(indexError)
                    return

                print('Host:', hostInfo['name'])
                print('XML File:', hostInfo['xmlFile'])
                for deviceName, deviceData in hostInfo['deviceList'].items():
                    print(deviceName)
                    for k, v in deviceData.items():
                        try:
                            v.has_key(False)
                        except:
                            print("\t%s: %s" % (k, v))
                print('')
                return

        elif action == 'info':
            output = hp.ENUM_HOSTS
            dataStructs = []
            for arg in argv[2:]:
                try:
                    arg = int(arg)
                except:
                    pass
                output = output[arg]
            try:
                for k, v in output.items():
                    try:
                        v.has_key(False)
                        dataStructs.append(k)
                    except:
                        print(k, ':', v)
                        continue
            except:
                print(output)

            for struct in dataStructs:
                print(struct, ': {}')
            return

        elif action == 'get':
            if argc == 3:
                try:
                    index = int(argv[2])
                    hostInfo = hp.ENUM_HOSTS[index]
                except:
                    print(indexError)
                    return

                if hostInfo is not None:
                    # If this host data is already complete, just display it
                    if hostInfo['dataComplete']:
                        print('Data for this host has already been enumerated!')
                        return

                    try:
                        # Get extended device and service information
                        if hostInfo:
                            print("Requesting device and service info for %s (this could take a few seconds)..." %
                                  hostInfo['name'])
                            print('')
                            if not hostInfo['dataComplete']:
                                (xmlHeaders, xmlData) = hp.getXML(hostInfo['xmlFile'])
                                if not xmlData:
                                    print('Failed to request host XML file:', hostInfo['xmlFile'])
                                    return
                                if not hp.getHostInfo(xmlData, xmlHeaders, index):
                                    print("Failed to get device/service info for %s..." % hostInfo['name'])
                                    return
                            print('Host data enumeration complete!')
                            hp.updateCmdCompleter(hp.ENUM_HOSTS)
                            return
                    except KeyboardInterrupt as e:
                        print("")
                        return

        elif action == 'send':
            # Send SOAP requests
            index = False
            inArgCounter = 0

            if argc != 6:
                showHelp(argv[0])
                return
            else:
                try:
                    index = int(argv[2])
                    hostInfo = hp.ENUM_HOSTS[index]
                except:
                    print(indexError)
                    return
                deviceName = argv[3]
                serviceName = argv[4]
                actionName = argv[5]
                actionArgs = False
                sendArgs = {}
                retTags = []
                controlURL = False
                fullServiceName = False

                # Get the service control URL and full service name
                try:
                    controlURL = hostInfo['proto'] + hostInfo['name']
                    controlURL2 = hostInfo['deviceList'][deviceName]['services'][serviceName]['controlURL']
                    if not controlURL.endswith('/') and not controlURL2.startswith('/'):
                        controlURL += '/'
                    controlURL += controlURL2
                except Exception as e:
                    print('Caught exception:', e)
                    print("Are you sure you've run 'host get %d' and specified the correct service name?" % index)
                    return False

                # Get action info
                try:
                    actionArgs = hostInfo['deviceList'][deviceName]['services'][serviceName]['actions'][actionName][
                        'arguments']
                    fullServiceName = hostInfo['deviceList'][deviceName]['services'][serviceName]['fullName']
                except Exception as e:
                    print('Caught exception:', e)
                    print("Are you sure you've specified the correct action?")
                    return False

                for argName, argVals in actionArgs.items():
                    actionStateVar = argVals['relatedStateVariable']
                    stateVar = hostInfo['deviceList'][deviceName]['services'][serviceName]['serviceStateVariables'][
                        actionStateVar]

                    if argVals['direction'].lower() == 'in':
                        print("Required argument:")
                        print("\tArgument Name: ", argName)
                        print("\tData Type:     ", stateVar['dataType'])
                        if stateVar.has_key('allowedValueList'):
                            print("\tAllowed Values:", stateVar['allowedValueList'])
                        if stateVar.has_key('allowedValueRange'):
                            print("\tValue Min:     ", stateVar['allowedValueRange'][0])
                            print("\tValue Max:     ", stateVar['allowedValueRange'][1])
                        if stateVar.has_key('defaultValue'):
                            print("\tDefault Value: ", stateVar['defaultValue'])
                        prompt = "\tSet %s value to: " % argName
                        try:
                            # Get user input for the argument value
                            (argc, argv) = getUserInput(hp, prompt)
                            if argv is None:
                                print('Stopping send request...')
                                return
                            uInput = ''

                            if argc > 0:
                                inArgCounter += 1

                            for val in argv:
                                uInput += val + ' '

                            uInput = uInput.strip()
                            if stateVar['dataType'] == 'bin.base64' and uInput:
                                uInput = base64.encodebytes(uInput)

                            sendArgs[argName] = (uInput.strip(), stateVar['dataType'])
                        except KeyboardInterrupt:
                            print("")
                            return
                        print('')
                    else:
                        retTags.append((argName, stateVar['dataType']))

                # Remove the above inputs from the command history
                while inArgCounter:
                    try:
                        readline.remove_history_item(readline.get_current_history_length() - 1)
                    except:
                        pass

                    inArgCounter -= 1

                # print 'Requesting',controlURL
                soapResponse = hp.sendSOAP(hostInfo['name'], fullServiceName, controlURL, actionName, sendArgs)
                if soapResponse:
                    # It's easier to just parse this ourselves...
                    for (tag, dataType) in retTags:
                        tagValue = hp.extractSingleTag(soapResponse, tag)
                        if dataType == 'bin.base64' and tagValue is not None:
                            tagValue = base64.decodebytes(tagValue)
                        print(tag, ':', tagValue)
            return

    showHelp(argv[0])
    return


# Save data
def save(argc, argv, hp):
    suffix = '%s_%s.mir'
    uniqName = ''
    saveType = ''
    fnameIndex = 3

    if argc >= 2:
        if argv[1] == 'help':
            showHelp(argv[0])
            return
        elif argv[1] == 'data':
            saveType = 'struct'
            if argc == 3:
                index = argv[2]
            else:
                index = 'data'
        elif argv[1] == 'info':
            saveType = 'info'
            fnameIndex = 4
            if argc >= 3:
                try:
                    index = int(argv[2])
                except Exception as e:
                    print('Host index is not a number!')
                    showHelp(argv[0])
                    return
            else:
                showHelp(argv[0])
                return

        if argc == fnameIndex:
            uniqName = argv[fnameIndex - 1]
        else:
            uniqName = index
    else:
        showHelp(argv[0])
        return

    fileName = suffix % (saveType, uniqName)
    if os.path.exists(fileName):
        print("File '%s' already exists! Please try again..." % fileName)
        return
    if saveType == 'struct':
        try:
            fp = open(fileName, 'w')
            pickle.dump(hp.ENUM_HOSTS, fp)
            fp.close()
            print("Host data saved to '%s'" % fileName)
        except Exception as e:
            print('Caught exception saving host data:', e)
    elif saveType == 'info':
        try:
            fp = open(fileName, 'w')
            hp.showCompleteHostInfo(index, fp)
            fp.close()
            print("Host info for '%s' saved to '%s'" % (hp.ENUM_HOSTS[index]['name'], fileName))
        except Exception as e:
            print('Failed to save host info:', e)
            return
    else:
        showHelp(argv[0])

    return


# Load data
def load(argc, argv, hp):
    if argc == 2 and argv[1] != 'help':
        loadFile = argv[1]

        try:
            fp = open(loadFile, 'r')
            hp.ENUM_HOSTS = {}
            hp.ENUM_HOSTS = pickle.load(fp)
            fp.close()
            hp.updateCmdCompleter(hp.ENUM_HOSTS)
            print('Host data restored:')
            print('')
            host(2, ['host', 'list'], hp)
            return
        except Exception as e:
            print('Caught exception while restoring host data:', e)

    showHelp(argv[0])


# Open log file
def log(argc, argv, hp):
    if argc == 2:
        logFile = argv[1]
        try:
            fp = open(logFile, 'a')
        except Exception as e:
            print('Failed to open %s for logging: %s' % (logFile, e))
            return
        try:
            hp.LOG_FILE = fp
            ts = []
            for x in time.localtime():
                ts.append(x)
            theTime = "%d-%d-%d, %d:%d:%d" % (ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])
            hp.LOG_FILE.write("\n### Logging started at: %s ###\n" % theTime)
        except Exception as e:
            print("Cannot write to file '%s': %s" % (logFile, e))
            hp.LOG_FILE = False
            return
        print("Commands will be logged to: '%s'" % logFile)
        return
    showHelp(argv[0])


# Show help
def help(argc, argv, hp):
    showHelp(False)


# Debug, disabled by default
def debug(argc, argv, hp):
    command = ''
    if not hp.DEBUG:
        print('Debug is disabled! To enable, try the set command...')
        return
    if argc == 1:
        showHelp(argv[0])
    else:
        for cmd in argv[1:]:
            command += cmd + ' '
        command = command.strip()
        print(eval(command))
    return


# Quit!
def exit(argc, argv, interface):
    quit(argc, argv, interface)


# Quit!
def quit(argc, argv, interface):
    if argc == 2 and argv[1] == 'help':
        showHelp(argv[0])
        return
    print('Bye!')
    print('')
    cleanup(interface)
    sys.exit(0)
