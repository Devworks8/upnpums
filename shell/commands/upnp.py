################## Action Functions ######################
# These functions handle user commands from the shell

import time

from shell.helpers import *


# from shell.helpers import *


# Actively search for UPNP devices
def msearch(argc, argv, hp):
    defaultST = "upnp:rootdevice"
    st = "schemas-upnp-org"
    myip = ''
    lport = hp.port

    if argc >= 3:
        if argc == 4:
            st = argv[1]
            searchType = argv[2]
            searchName = argv[3]
        else:
            searchType = argv[1]
            searchName = argv[2]
        st = "urn:%s:%s:%s:%s" % (st, searchType, searchName, hp.UPNP_VERSION.split('.')[0])
    else:
        st = defaultST

    # Build the request
    request = "M-SEARCH * HTTP/1.1\r\n" \
              "HOST:%s:%d\r\n" \
              "ST:%s\r\n" % (hp.ip, hp.port, st)
    for header, value in hp.msearchHeaders.items():
        request += header + ':' + value + "\r\n"
    request += "\r\n"

    print("Entering discovery mode for '%s', Ctl+C to stop..." % st)
    print('')

    # Have to create a new socket since replies will be sent directly to our IP, not the multicast IP
    server = hp.createNewListener(myip, lport)
    if not server:
        print('Failed to bind port %d' % lport)
        return

    hp.send(request, server)
    count = 0
    start = time.time()

    while True:
        try:
            if 0 < hp.MAX_HOSTS <= count:
                break

            if 0 < hp.TIMEOUT < (time.time() - start):
                raise Exception("Timeout exceeded")

            if hp.parseSSDPInfo(hp.recv(1024, server), False, False):
                count += 1

        except Exception as e:
            print('\nDiscover mode halted...')
            break


# Passively listen for UPNP NOTIFY packets
def pcap(argc, argv, hp):
    print('Entering passive mode, Ctl+C to stop...')
    print('')

    count = 0
    start = time.time()

    while True:
        try:
            if 0 < hp.MAX_HOSTS <= count:
                break

            if 0 < hp.TIMEOUT < (time.time() - start):
                raise Exception("Timeout exceeded")

            if hp.parseSSDPInfo(hp.recv(1024, False), False, False):
                count += 1

        except Exception as e:
            print("\nPassive mode halted...")
            break


# Manipulate M-SEARCH header values
def head(argc, argv, hp):
    if argc >= 2:
        action = argv[1]
        # Show current headers
        if action == 'show':
            for header, value in hp.msearchHeaders.items():
                print(header, ':', value)
            return
        # Delete the specified header
        elif action == 'del':
            if argc == 3:
                header = argv[2]
                if hp.msearchHeaders.has_key(header):
                    del hp.msearchHeaders[header]
                    print('%s removed from header list' % header)
                    return
                else:
                    print('%s is not in the current header list' % header)
                    return
        # Create/set a headers
        elif action == 'set':
            if argc == 4:
                header = argv[2]
                value = argv[3]
                hp.msearchHeaders[header] = value
                print("Added header: '%s:%s" % (header, value))
                return

    showHelp(argv[0])
