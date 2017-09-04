# vbox-backup

A tool to backup VirtualBox machines

Notes:
- maybe use this as a starting point: https://askubuntu.com/questions/935850/automated-virtual-machine-backups-on-ubuntu-virtualbox
- https://superuser.com/questions/878011/what-is-the-difference-between-virtualbox-sav-and-vdi-files
- https://github.com/PythonNut/virtualbox-remote-snapshots

use python or bash?

make a service for it, run every how long?
have a way to pause the shutdowns for a period of time if important things are happening?
how to handle errors in command all the way back up to the main function, what does each mean, retry? catch specifics?


Process:
- lookup list of VM's to backup (which? running ones, from a list, in a file, in this code? in parameters?)
- Lookup list of available vms: `vboxmanage list vms` or `vboxmanage list runningvms`
- look at what snapshots are listed for the VM, one proceed if one hasn't been taken since ??? `VBoxManage snapshot...`. Maybe use export?
- Safely Poweroff the VM in question (do we have to???):`VBoxManage controlvm <vm> acpipowerbutton`, is there a way to check that it has been powered off? wait x seconds? maybe move on to force shutdown
- take snapshot, name it something with date in it (to be used in lookup?) 
- rsync it to a remote location (what type of backup, incremental?)
- remove older backups?
- turn the vm back on again
- move onto the next VM to backup
