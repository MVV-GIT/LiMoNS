import http.client
import os
import sys
from datetime import datetime

import docker
import psutil

version = '0.1.1.37'

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


def get_process_info():
    process_list = {}
    for proc in psutil.process_iter():

        try:
            process_list.update({proc.pid: proc.name()})
            proc.name()
        except psutil.NoSuchProcess:
            pass

    return(process_list)

def get_sys_state():
    sys_state = {}

def get_docker_state():
    docker_state = {}
    run_dockers = docker.from_env()
    run_dockers.reload()
    for containerx in run_dockers.containers.list():
        docker_state.update({containerx : [{'Name': containerx.attrs['Name']},{'Status': containerx.attrs['State']['Status']},{'Image':containerx.attrs['Config']['Image']}]})
    return docker_state

def get_cpu_percent_short(all_cpu = True):
    return psutil.cpu_percent(None, all_cpu)

def get_cpu_percent_full(all_cpu = True):
    return psutil.cpu_times_percent(None, all_cpu)

def det_mem_full():
    return psutil.virtual_memory()

def det_swap_mem_full():
    return psutil.swap_memory()

def get_disk_info_full(all_disk = True):
    return psutil.disk_partitions(all_disk)

def get_net_info_full(all_interface = True):
    return psutil.net_io_counters(all_interface)

def get_net_connections_info_full(inet_connect = 'inet'):
    return psutil.net_connections(inet_connect)

def get_net_addr_info():
    return psutil.net_if_addrs()

def get_net_stat_info():
    return psutil.net_if_stats()

def get_users_info():
    return psutil.users()

def get_boot_time_info():
    return psutil.boot_time()

def get_sys_info():

    sys_info_set = {}

    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    nodeip = str(conn.getresponse().read())
    system_time_stamp = datetime.now()

    sys_info_set = {
        {'Scrypt_Name'}: 'LInux MOnitoring Node Symbol scrypt.',
        {'Scrypt_Version'}:version,
        {'Python_Version'}: str(sys.version_info.major) + '.' + str(sys.version_info.minor),
        {'OS'}: str(sys.platform) + '/' + str(os.name),
        {'Node_IP'}: nodeip[2:-1],
        {'CPU_Core'}: str(psutil.cpu_count(logical=False)),
        {'CPU_Thread'}: str(psutil.cpu_count(logical=True)),
        {'CPU_Arch'}: os.getenv('PROCESSOR_ARCHITECTURE'),
        {'CPU_ID'}: str(os.getenv('PROCESSOR_IDENTIFIER')),
        {'CPU_Level'}:str(os.getenv('PROCESSOR_LEVEL')),
        {'Local_time_stamp'}: system_time_stamp.astimezone().strftime('%Y-%m-%d %H:%M:%S [%z]')
    }
    return sys_info_set

def print_sys_info():
    info = get_sys_info()

    print('Scrypt version:', info['Scrypt_Name'], info['Scrypt_Version'])
    print('Python version:', info['Python_Version'])
    print('OS:',  info['OS'])
    print('Node IP:', info['Node_IP'])
    print('CPU:',   info['CPU_Core'])
    print('CPU:',   info['CPU_Thread'])
    print('CPU:',   info['CPU_Arch'])
    print('CPU:',   info['CPU_ID'])
    print('CPU:',   info['CPU_Level'])
    print('Local time: ', info[''])


def scr_set0(cstr=0):
        for _ in range(0..cstr):
            print('\033[F\033[K', end='')