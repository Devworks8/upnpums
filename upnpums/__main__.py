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

# from shell.taskmanager import *
from config.configure import *
from database.dbparser import *
from shell.commandmanager import *
import multitasking
import signal

__VERSION__ = "0.1"

signal.signal(signal.SIGINT, multitasking.killall)


# multitasking.set_engine("process")

# Main
@multitasking.task
def main(argc, argv):
    # Initialize the Task Manager
    # tm = TaskManager()

    # Initialize the Config
    cm = CfgManager()

    """
    if cm.get('threading_exit')[0][1] is 'killall':
        signal.signal(signal.SIGINT, multitasking.killall)
    else:
        signal.signal(signal.SIGINT, multitasking.wait_for_tasks)
    """


    # Initialize the Database
    dm = DbParser(config=cm)

    # Initilize the shell class
    sh = CmdManager(config=cm, db=dm)
    sh.start(argc, argv, interface=sh, config=cm, db=dm)

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
