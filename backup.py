# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import subprocess, sys, argparse, re, datetime, virtualbox

vbox = virtualbox.VirtualBox()

#parse input arguments -m, method, -l, limit
parser = argparse.ArgumentParser()

#add arguments for time between snapshots, remote snapshot retention policy, remote location to store
parser.add_argument('-v','--vm', nargs='+', help='Which VMs to process')
parser.add_argument('-f','--file', help='Path to file containing list of VM names to process')
parser.add_argument('-t','--time', help='Time, in seconds, between when snapshots should be taken')
parser.add_argument('-a', '--all', action='store_true', help='Boolean, whether to process all vms')

#TODO: add in -a all arguement, add an arguement for time between snapshots. configure it so you cant pass in all with specific other vms to process


# Use like:
# python arg.py -l 1234 2345 3456 4567
#nargs='+' takes 1 or more arguments, nargs='*' takes zero or more.

args = parser.parse_args()

inputVMList = []

#the time allowed before another snapshot should be taken (in seconds)
timeBetweenSnapshots = 604800

print(args)

if args.vm:
    for value in args.vm:
        if value is not None:
            print(value)
            inputVMList.append(value)
if args.file:
    file = args.file
    print("File name: ", file)
    #TODO: lookup list of VMs in file, check they haven't already been added to input list, append them to input list
if args.time:
    timeBetweenSnapshots = args.time

#no CLI input was provided
if not args.file and not args.vm:
    #look for list in file (should you have to pass in a file name?)
    print("No CLI arguments")

    #TODO: quit here as there is nothing to do

#print(inputVMList)

vmList = []

class vmItem:
    def __init__(self, name, uuid, initialState):
        self.name = name
        self.initialState = initialState
        self.isRunning = initialState
        self.uuid = uuid
        #TODO: probably want to add in details about when last snapshot was taken

    def helloWorld(self):
        print("This VM is called: {}".format(self.name))

    def isRunning(self):
        print("Checking whether this VM is running")

    #Check whether the current VM is due for a new snapshot
    def needsSnapshot(self):
        #print("We should take a snapshot")

        vm = vbox.find_machine(self.name)

        print("Found VM {}".format(vm.name))

        with vm.create_session() as session:
            print("Session created for VM {}".format(vm.name))

            #print(session.machine.current_snapshot)
            #will be null if no current snapshot
            if not session.machine.current_snapshot:
                print("There are current no snapshots for {}".format(vm.name))
                return True
            else:
                snapshotTime = session.machine.current_snapshot.time_stamp
                print("Current snapshot for {} was taken {}".format(vm.name, snapshotTime))

                # TODO: current_state_modified
                # Get bool value for 'currentStateModified' Returns true if the current state of the machine is
                # not identical to the state stored in the current snapshot.

                #another snapshot is needed
                if snapshotTime > timeBetweenSnapshots:
                    print('It has been {} seconds since the last snapshot. Another is required'.format(snapshotTime - timeBetweenSnapshots))
                    return True
                else: return False

    def takeSnapshot(self):
        vm = vbox.find_machine(self.name)

        with vm.create_session() as session:
            print("Session created for VM {}".format(vm.name))

            #TODO: configure takeing a snapshot
            #command = ['VBoxManage', 'snapshot', 'take', vm.name + ' - ' + date.current,'--details']

            currentTime = datetime.datetime.now()
            snapshotName = vm.name + ' - snapshot - ' + str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day)

            try:
                print("Taking snapshot of {}...".format(vm.name))
                progress = session.machine.take_snapshot(snapshotName,'',True)

            except Exception as e:
                #print("Failed to create directory for saved state file.")
                print("Unknown error attempting to take a snapshot of VM {}: {}".format(vm.name, e))
                return
            except:
                e = sys.exc_info()[0]
                print("Unknown error attempting to take a snapshot of VM {}: {}".format(vm.name, e))

            #TODO: check that the VM snapshot was taken successfully. can I validate it? is it now the current snapshot?

            #TODO; probably want to migrate away from `process[0]` being referenced explicitly in the long run
            #print("Snapshot progress: {}".format(progress[0].percent()))

            #TODO: probably want to use wait_for_completion(timeout=-1)

            try:
                print("Attempting to wait for process completion")
                progress[0].wait_for_completion(-1)
                print('process has now been completed')

                #check if the current snapshot state is the same as the VM (not modified), this means the latest snapshot represents the current state of the VM
                if not session.machine.current_state_modified:
                    print("The current state of the VM {} is the same as the current snapshot. This means the snapshot that was taken was successful".format(vm.name))
                    return

            except:
                print("Failed to wait for snapshot completion")


    def startVM(self):
        vm = vbox.find_machine(self.name)
        print("Found VM {}".format(vm.name))

        with vm.create_session() as session:
            print("Session created for VM {}".format(vm.name))

            print("Starting VM {}".format(vm.name))

            try:
                #session.machine.launch_vm_process()
                progress = vm.launch_vm_process(session, 'headless', '')
            except:
                e = sys.exc_info()[0]
                print("Unknown error attempting to start VM {}: {}".format(vm.name, e))

            #TODO: check that VM is now started

            try:
                print("Attempting to wait for process completion")
                progress.wait_for_completion(-1)
                print('process has now been completed')

                #TODO: check that the VM is actaually running
                return

            except:
                e = sys.exc_info()[0]
                print("Failed to wait for vm {} to start: {}".format(vm.name, e))


    def stopVM(self):
        vm = vbox.find_machine(self.name)
        print("Found VM {}".format(vm.name))

        with vm.create_session() as session:
            print("Session created for VM {}".format(vm.name))

            #TODO: is there a cleaner way to poweroff the machine? maybe by logging in?
            #Safely Poweroff the VM in question (do we have to???):`VBoxManage controlvm <vm> acpipowerbutton`, is there a way to check that it has been powered off? wait x seconds? maybe move on to force shutdown
            print("Stopping VM {}".format(vm.name))
            try:
                #TODO: maybe should use power_down() function
                #session.console.power_button()
                progress = session.console.power_down()
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
                progress.wait_for_completion(-1)
                print('Shutdown has now been completed')

            except:
                e = sys.exc_info()[0]
                print("Failed to wait for vm {} to start: {}".format(vm.name, e))

    #def remoteBackupVM():
        #TODO: rsync it to a remote location (what type of backup, incremental?)
        #remove older backups?


#get a list of VMs in VirtualBox
def getVMList():

    outputList = []
    listIsEmpty = True

    #TODO: loop through the list of inputted VMs and only add the ones on the list to the array

    #loop through the list of VMs
    for vm in vbox.machines:
        #print(vm.name, ' ', vm.id_p, ' ', vm.state)

        #TODO: add in lookup for running vm here

        for inputVM in inputVMList:

            #keep processing if the VM being looked at was requested
            if vm.name == inputVM:

                vmState = str(vm.state)
                #print(type(vmState))
                if vmState != 'Running':
                    print('VM {} is not running'.format(vm.name))
                    isRunning = False
                else:
                    print('VM {} is running'.format(vm.name))
                    isRunning = True

                v = vmItem(vm.name,vm.id_p, isRunning)
                vmList.append(v)

def main():

    #create a structure of available vms, mark each as running or not
    getVMList()

    for vm in vmList:

        #print(vm.name)
        #print(vm.initialState)
        #print(vm.isRunning)

        #vm.helloWorld()

        #continue if the VM needs a snapshot
        if vm.needsSnapshot():

            print("The VM '{}' needs a new snapshot.".format(vm.name))

            if vm.isRunning:
                vm.stopVM()

            #take snapshot
            vm.takeSnapshot()

            #the VM was started at the beggining of the process, but is not started now. This VM needs to be started.
            if not vm.isRunning and vm.initialState:
                vm.startVM()

            #rsync the snapshot to a remote location
            #backupVM()


if __name__ == "__main__":
    main()
