import os
import sys
import http.client
from datetime import datetime

import psutil
import tzlocal


version = '0.1.0.23'

# color scheme
c_black = '\033[30m'  # black
c_red = '\033[31m'  # red
c_green = '\033[32m'  # green
c_yellow = '\033[33m'  # yellow
c_blue = '\033[34m'  # blue
c_magenta = '\033[35m'  # magenta
c_cyan = '\033[36m'  # cyan
c_white = '\033[37m'  # white
c_norm = '\033[39m'
cb_white = '\033[47m'
cb_norm = '\033[49m'


def sys_info(disp=False, log=False):

    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    nodeip = str(conn.getresponse().read())

    print('LInux MOnitoring Node Symbol scrypt. V.' + version)
    print('Python V.' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + ' installed')
    print('OS: ' + str(sys.platform) + '/' + str(os.name))
    print('Node IP: ' + nodeip[2:-1])
    print('CPU: [core:' + str(psutil.cpu_count(logical=False)) + ' / thread:' + str(
        psutil.cpu_count(logical=True)) + '] Arch:' + str(
        os.getenv('PROCESSOR_ARCHITECTURE')) + ' CPUID:'
          + str(os.getenv('PROCESSOR_IDENTIFIER'))
          + ', CPU level:' + str(os.getenv('PROCESSOR_LEVEL')))

    local_tz = tzlocal.get_localzone()
    totaltimestart = datetime.now()
    print('Local time: ' + local_tz.fromutc(totaltimestart).strftime('%Y-%m-%d %H:%M:%S [%z]'))
    exit(0)

def scr_set0(cstr=0):
        for _ in range(0..cstr):
            print('\033[F\033[K', end='')