import http.client
import os
import sys
from datetime import datetime
import psutil
import tzlocal

version = '0.1.0.0'

conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
nodeip = str(conn.getresponse().read())

print('LInux MOnitoring Node Symbol scrypt. V.' + version)
print('Python V.' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + ' installed')
print('OS: ' + str(sys.platform) + '/' + str(os.name))
print('Node IP: ' + nodeip[2:-1])
print('CPU: [core:' + str(psutil.cpu_count(logical=False))  + ' / thread:' + str(psutil.cpu_count(logical=True))  + '] Arch:' + str(
    os.getenv('PROCESSOR_ARCHITECTURE')) + ' CPUID:'
      + str(os.getenv('PROCESSOR_IDENTIFIER')) + ', CPU level:' + str(os.getenv('PROCESSOR_LEVEL')))

local_tz = tzlocal.get_localzone()
totaltimestart = datetime.now()
print('Local time: ' + local_tz.fromutc(totaltimestart).strftime('%Y-%m-%d %H:%M:%S [%z]'))
exit(0)