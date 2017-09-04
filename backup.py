import subprocess, sys, argparse


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
    def __init__(self, name):
        self.name = name
        isStarted = False
        
    


def printDF():
    
    command = ['df', '-h']
    
    output = callCommand(command)

    
    output = str(output)
    #print(str(output))
    output = output.split('\\n')
    #print(output)
    #print('Type: ', type(output))
    #print(output[0])
    
#printDF()
    


# time = callCommand('date')
# print('It is', time)
# print('Type: ', type(time))


def getVMList():
    
    command = 'vboxmanage list vms'
    
    output = callCommand(command)
    
    output = str(output)
    print(output)
    #output = output.split('\\n')
    
    #what is the output? filter down to just the names of the VMs
    
    #can I see that the VM is running in this step?
    
    for vm in output:
        v = vmItem(vm)
        vmList.append(v)
    
    return

def getRunningVMList():
    
    runningVMList = []
    
    command = 'vboxmanage list runningvms'
    
    output = callCommand(command)
    
    output = str(output)
    print(output)
    #output = output.split('\\n')
    
    #what is the output? filter down to just the names of the VMs
    
    for outputItem in output:
        for vm in vmList:
            if vm.name == outputItem:
                vm.isRunning = True
    
    for vm in output:
        v = vmItem(vm)
        runningVMList.append(v)
    
    runningVMList = subprocess.call('vboxmanage list runningvms')

def getSnapshotList():
    #snapshotList = subprocess.call('VBoxManage snapshot list')
    #snapshotList = subprocess.call(['VBoxManage snapshot list', '--details'])
    
    command = ['VBoxManage snapshot list', '--details']
    
    output = callCommand(command)

def checkNeedsSnapshot():
    snapshotList = getSnapshotList()
    
    needsSnapshot = False
    
    #loop through each snapshot, check if any more recent than min date between snapshots
    for snapshot in snapshotList:
        if (today.date - snapshot.date) < inputRetention:
            needsSnapshot = True
    
    return needsSnapshot
    
def takeSnapshot():
    #take snapshot, name it something with date in it (to be used in lookup?)
    #snapshotList = subprocess.call('VBoxManage snapshot list')
    
    command = ['VBoxManage snapshot list', '--details']
    
    output = callCommand(command)
    
    
def backupVM():
    #rsync it to a remote location (what type of backup, incremental?)
    #remove older backups?
    print("hello world")
    
def powerOffVM():
    #subprocess.call('VBoxManage controlvm' + vm + 'acpipowerbutton')
    
    command = 'VBoxManage controlvm' + vm + 'acpipowerbutton'
    
    output = callCommand(command)
    
def startVM():
    #subprocess.call('VBoxManage startvm' + vm)
    
    command = 'VBoxManage startvm' + vm
    
    output = callCommand(command)
    
def whichVMs():
    
    vmList = getVMList()
    
    runningVMList = getRunningVMList()
    
    #append items to vmList
    
    

def main():
    
    #create a structure of available vms, mark each as running or not
    
    whichVMs()
    
    
    for vm in vmList:
        #look at what snapshots are listed for the VM, one proceed if one hasn't been taken since ??? `VBoxManage snapshot...`. Maybe use export? maybe include `--details`
        
        #find last date? if statement to continue
        if checkNeedsSnapshot():
            
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