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

from config.configure import *
from database.dbparser import *
from shell.commandmanager import *
import multitasking
import signal

__VERSION__ = "0.1"

# Initialize the Config
cm = CfgManager()

# Set the threads exit behavior
if cm.get('threading_exit')[0][1] == 'wait':
    signal.signal(signal.SIGINT, multitasking.wait_for_tasks)
else:
    signal.signal(signal.SIGINT, multitasking.killall)

# Set the engine
if cm.get('threading_engine')[0][1] == 'process':
    multitasking.set_engine('process')


# Main
@multitasking.task
def main(argc, argv, config):
    # Initialize the Database
    dm = DbParser(config=config)

    # Initialize the shell class
    sh = CmdManager(config=config, db=dm)
    sh.start(argc, argv, interface=sh, config=config, db=dm)

    # Initialize upnp class
    # hp = Upnp(False, False, None, appCommands);


if __name__ == "__main__":
    try:
        print('')
        print('UPnPUMS v%s' % __VERSION__)
        print('The interactive UPnP Universal Media Server')
        print('Christian Lachapelle & Jason Major')
        print('')
        main(len(sys.argv), sys.argv, config=cm)

    except Exception as e:
        print('Caught main exception:', e)
        sys.exit(1)
