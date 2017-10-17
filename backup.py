import subprocess, sys, argparse, re, time


#parse input arguments -m, method, -l, limit
parser = argparse.ArgumentParser()

#add arguments for time between snapshots, remote snapshot retention policy, remote location to store
parser.add_argument('-v','--vm', nargs='+', help='Which VMs to process')
parser.add_argument('-f','--file', help='path to file containing list of VM names to process')

# Use like:
# python arg.py -l 1234 2345 3456 4567
#nargs='+' takes 1 or more arguments, nargs='*' takes zero or more.

args = parser.parse_args()

inputVMList = []

print(args)




if args.vm:
    for value in args.vm:
        if value is not None:
            print(value)
            inputVMList.append(value)
if args.file:
    file = args.file
    print("File name: ", file)
    #lookup list of VMs in file, check they haven't already been added to input list, append them to input list
#no CLI input was provided
if not args.file and not args.vm:
    #look for list in file (should you have to pass in a file name?)
    print("No CLI arguments")
    #readVMFile()

#print(inputVMList)

def callCommand(commandInput):
    try:
        command = subprocess.Popen(commandInput, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = command.communicate()

        return output

    except:
        e = sys.exc_info()[0]
        print("Running command `", commandInput, "` returned the following error: ", e)



#find list of VMs to process backup for

#lookup vms from file? accept parameter?

vmList = []

class vmItem:
    def __init__(self, name, uuid):
        self.name = name
        self.isStarted = False
        self.uuid = uuid




def printDF():

    command = ['df', '-h']

    output = callCommand(command)


    output = str(output)
    #print(str(output))
    output = output.split('\\n')
    #print(output)
    #print('Type: ', type(output))
    #print(output[0])


#get a list of VMs in VB
def getVMList():

    outputList = []
    listIsEmpty = True

    command = ['vboxmanage', 'list', 'vms']

    output = callCommand(command)

    output = output[0]
    #print(output)

    output = output.decode('utf-8')
    output = output.rstrip("\n")
    output = output.split('\n')
    #print(output)
    #check that there are items in the list of VMs
    for item in output:
        if item:
            name = re.search(r'"([^"]*)"', item)
            name = name.group(1).strip('"')
            print("name: ", name)

            uuid = re.search(r'{([^"]*)}', item)
            uuid = uuid.group(1).rstrip('}')
            uuid = uuid.lstrip('{')
            print("uuid: ", uuid)

            v = vmItem(name,uuid)
            vmList.append(v)

    #output = str(output[0])
    #print(output)
    #print(type(output))
    #strip off the extra characters on the left and right
    #output = output.lstrip("b'")
    #output = output.rstrip("\\n'")
    #print(output)

    #split the string at the new line to seperate entries
    #output = output.split('\\n')

    #loop through each of the items in the list of returned entries
    # for outputItem in outputList:
    #     print("outputItem: ", outputItem)
    #
    #     #pull the name of the VM out from within the quotes
    #     name = re.search(r'"([^"]*)"', outputItem)
    #     name = name.group(1).strip('"')
    #     #print("name: ", name)
    #
    #     #print("outputItem: ", outputItem)
    #
    #     #pull the uuid out from within the {}
    #     uuid = re.search(r'{([^"]*)}', outputItem)
    #     uuid = uuid.group(1).rstrip('}')
    #     uuid = uuid.lstrip('{')
    #     #print("uuid: ", uuid)
    #
    #     v = vmItem(name,uuid)
    #     vmList.append(v)


def getRunningVMList():

    outputList = []
    listIsEmpty = True

    runningVMList = []

    command = ['vboxmanage', 'list', 'runningvms']

    output = callCommand(command)

    output = output[0]
    print(output)

    output = output.decode('utf-8')
    output = output.rstrip("\n")
    output = output.split('\n')
    print(output)
    print(type(output))
    #check that there are items in the list of VMs
    for item in output:
        if item:
            name = re.search(r'"([^"]*)"', item)
            name = name.group(1).strip('"')
            print("name: ", name)

            for vm in vmList:
                if vm.name == name:

                    vm.isRunning = True


def getSnapshotList(vm):
    command = ['VBoxManage', 'snapshot', vm.name ,'list', '--details', '--machinereadable']

    output = callCommand(command)

    print('getSnapshotList output:')
    print(output)

    output = output[0]

    output = output.decode('utf-8')
    output = output.rstrip('\n')
    output = output.split('\n')

    print(output)
    print(type(output))

    snapshotList = []

    for snapshot in output:
        print("snapshot:")
        print(snapshot)
        snapshot = snapshot.rstrip('"')
        snapshot = snapshot.split('="')
        print(snapshot)

        if snapshot[0] != "CurrentSnapshotUUID" or snapshot[0] != "CurrentSnapshotNode":
            


    return output

def checkNeedsSnapshot(vm):
    snapshotList = getSnapshotList(vm)

    needsSnapshot = False

    #if the response is `This machine does not have any snapshots` then it doesnt need a snaotshot

    #loop through each snapshot, check if any more recent than min date between snapshots
    for snapshot in snapshotList:
        #if (today.date - snapshot.date) < inputRetention:
        #    needsSnapshot = True
        print("snapshot:")
        print(snapshot)
        snapshot = snapshot.rstrip('"')
        snapshot = snapshot.split('="')
        print(snapshot)

    return needsSnapshot

def takeSnapshot(vm):
    #take snapshot, name it something with date in it (to be used in lookup?)
    #snapshotList = subprocess.call('VBoxManage snapshot list')

    command = ['VBoxManage', 'snapshot', 'take', vm.name + ' - ' + date.current,'--details']

    output = callCommand(command)


def backupVM(vm):
    #rsync it to a remote location (what type of backup, incremental?)
    #remove older backups?
    print("hello world")

def powerOffVM(vm):
    #subprocess.call('VBoxManage controlvm' + vm + 'acpipowerbutton')

    command = ['VBoxManage', 'controlvm', vm.name, 'acpipowerbutton']

    output = callCommand(command)

def startVM(vm):
    #subprocess.call('VBoxManage startvm' + vm)

    command = ['VBoxManage','startvm', vm.name]

    output = callCommand(command)

def whichVMs():

    getVMList()

    getRunningVMList()



def main():

    #create a structure of available vms, mark each as running or not

    whichVMs()


    for vm in vmList:

        # only run through this is there are listed vm arguements
        if inputVMList:

            for inputvm in inputVMList:

                #keep going is this vm was listed as an arguement
                if inputvm == vm.name:
                    #look at what snapshots are listed for the VM, one proceed if one hasn't been taken since ??? `VBoxManage snapshot...`. Maybe use export? maybe include `--details`

                    #print("Processing VM: ", vm.name)

                    #find last date? if statement to continue
                    if checkNeedsSnapshot(vm):

                        print("The VM ", vm, " needs a new snapshot.")

                        #Safely Poweroff the VM in question (do we have to???):`VBoxManage controlvm <vm> acpipowerbutton`, is there a way to check that it has been powered off? wait x seconds? maybe move on to force shutdown
                        #powerOffVM()

                        #take snapshot
                        #takeSnapshot()



                        #turn the vm back on again
                        #startVM()

                        #rsync it to a remote location (what type of backup, incremental?)
                        #remove older backups?
                        #backupVM()


if __name__ == "__main__":
    main()
