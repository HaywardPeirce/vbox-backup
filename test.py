from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import vboxapi
from vboxapi.VirtualBox_constants import VirtualBoxReflectionInfo
vboxMgr = vboxapi.VirtualBoxManager(None, None)
vbox = vboxMgr.vbox

vm = vbox.findMachine('Windows 7')
session = vboxMgr.openMachineSession(vm)

print(vm)
