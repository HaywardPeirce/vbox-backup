# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import subprocess, sys, argparse, re, datetime, virtualbox, time

vbox = virtualbox.VirtualBox()

vm = vbox.find_machine('Windows 7')
print("Found VM {}".format(vm.name))

with vm.create_session() as session:
    print("Session created for VM {}".format(vm.name))

    #TODO: is there a cleaner way to poweroff the machine? maybe by logging in?
    #Safely Poweroff the VM in question (do we have to???):`VBoxManage controlvm <vm> acpipowerbutton`, is there a way to check that it has been powered off? wait x seconds? maybe move on to force shutdown
    print("Stopping VM {}".format(vm.name))
    try:
        #TODO: maybe should use power_down() function
        #session.console.power_button()
        #progress = session.console.power_down()
        progress = session.console.power_button()
    except VBoxErrorPdmError as e:
        print("Unable to perform controlled power off")
    except:
        e = sys.exc_info()[0]
        print("Unknown error attempting to power off VM {}: {}".format(vm.name, e))

    #TODO: check that the VM is now stopped
    #vmState = str(vm.state)
    #print("The VM {} is current {}".format(vm.name, vmState))

    try:
        print("Attempting to wait for shutdown completion")
        progress[0].wait_for_completion(-1)
        print('Shutdown has now been completed')

    except:
        e = sys.exc_info()[0]
        print("Failed to wait for vm {} to start: {}".format(vm.name, e))
