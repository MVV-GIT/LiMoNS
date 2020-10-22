import http.client
import os
import sys
from datetime import datetime

import docker
import psutil


version = '0.1.0.0'

# conn = http.client.HTTPConnection("ifconfig.me")
# conn.request("GET", "/ip")
# nodeip = str(conn.getresponse().read())
#
# totaltimestart = datetime.now()
# print('LInux MOnitoring Node Symbol scrypt. V.' + version)
# print('Python V.' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + ' installed')
# print('OS: ' + str(sys.platform) + '/' + str(os.name))
# print('Node IP: ' + nodeip[2:-1])
# print('CPU: [core:' + str(psutil.cpu_count(logical=False))  + ' / thread:' + str(psutil.cpu_count(logical=True))  + '] Arch:' + str(
#     os.getenv('PROCESSOR_ARCHITECTURE')) + ' CPUID:'
#       + str(os.getenv('PROCESSOR_IDENTIFIER')) + ', CPU level:' + str(os.getenv('PROCESSOR_LEVEL')))
# print('Local time: ', totaltimestart.astimezone().strftime('%Y-%m-%d %H:%M:%S [%z]'))
#
# exit(0)

# print('Short CPU:', psutil.cpu_percent(1, True))
# print('Tuple CPU: ', psutil.cpu_times_percent(1, True))
# print('Mem :', psutil.virtual_memory())
# print('SwapMem :', psutil.swap_memory())
# print('Disc info:', psutil.disk_partitions(False))
# # print('Net info:', psutil.net_io_counters(True))
# # print('Connections info:',psutil.net_connections('inet'))
# # print('Net addr info:', psutil.net_if_addrs())
# print('NEt stat info:', psutil.net_if_stats())
# print('USers info:', psutil.users())
# print('Boot time  info:', psutil.boot_time())
#
#
# print('Mem :', psutil.virtual_memory())
# print('SwapMem :', psutil.swap_memory())
# mem = psutil.virtual_memory()
# print(mem[0])
# print(mem[1])
# print(mem[2])
# print(mem[3])
# print(mem[4])
#
# print(psutil.cpu_percent(None, False))

# client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# run_dockers = docker.from_env()
#
# for containerx in run_dockers.containers.list():
#     print(containerx, 'Name: [', containerx.attrs['Name'], '] Status: [',
#           containerx.attrs['State']['Status'], '] Image [', containerx.attrs['Config']['Image'])
#
#
#
# print('='*60)
#
# run_dockers.containers.list([0])
#
#
# container = run_dockers.containers.get('2af057d5c2')
#
# for line in container.logs(stream=True):
#     print(line.strip())


# >>> client.containers.list()
# [<Container '45e6d2de7c54'>, <Container 'db18e4f20eaa'>, ...]
#
# >>> container = client.containers.get('45e6d2de7c54')
#
# >>> container.attrs['Config']['Image']
# "bfirsh/reticulate-splines"
#
# >>> container.logs()
# "Reticulating spline 1...\n"
#
# >>> container.stop()
#
# process_list = {}
# for proc in psutil.process_iter():
#
#     try:
#         pinfo = proc.as_dict(attrs=['pid', 'name'])
#         process_list.update({proc.pid:proc.name()})
#         proc.name()
#     except psutil.NoSuchProcess:
#         pass
#
#
# print(process_list)

#
#
# for proc in psutil.process_iter():
#     try:
#         pinfo = proc.as_dict(attrs=['pid', 'name'])
#     except psutil.NoSuchProcess:
#         pass
#     else:
#         print(pinfo)
#
#
# print('kernel', int(psutil.cpu_times()[2]),'idle', int(psutil.cpu_times()[3]),'user',
#       int(psutil.cpu_times()[0]),'iowait', int(psutil.cpu_times()[4]),
#       'frequency', psutil.cpu_freq())

# docker_state = []
# run_dockers = docker.from_env()
# for containerx in run_dockers.containers.list():
#       docker_state.append([containerx, containerx.attrs['Name'], containerx.attrs['State']['Status'],containerx.attrs['Config']['Image']])
#
# print(len(docker_state))


# print(psutil.virtual_memory())
dcpuall = psutil.cpu_percent(None, True)

for i in range(len(dcpuall)):
    print('Core ' + str(i) + ' usage = ', dcpuall[i])
