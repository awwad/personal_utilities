# <~> Monitor memory pressure (active page pressure, inactive page pressure).

# Modified from a script provided by ... er, gotta track it down again. A post on serverfault.
#import os
#import sys
import re
import time
import subprocess

PERIODIC = 2

#pgs = re.compile('Pages active:\s+([0-9]+).\nPages inactive:\s+([0-9]+).')
#pgs = re.compile("b\'Pages active:\s*(\d+)\.\\\\nPages inactive:\s*(\d+)\.")

#meminfo = open('/proc/meminfo')
#meminfo 

def read_meminfo():
    #content = #meminfo.read(4096)
    content = str(subprocess.check_output(['vm_stat | grep active'],shell=True))

    #m = pgs.search(content, re.M)
    m = re.match("b\'Pages active:\s*(\d+)\.\\\\nPages inactive:\s*(\d+)\.",content)

    active, inactive = int(m.group(1)), int(m.group(2))
    active = active / 4
    inactive = inactive / 4
    #meminfo.seek(0,0)
    return active,inactive

if __name__ == "__main__":
    oldin, oldac = read_meminfo()
    while True:
        time.sleep(PERIODIC)
        active, inactive = read_meminfo()
        print("Inactive Pressure:\t"+str(inactive - oldin)+"\t\tActive Pressure:\t"+str(active - oldac))
        oldac = active
        oldin = inactive
