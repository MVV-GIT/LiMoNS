import http.client
import os
import sys
from datetime import datetime, timedelta
import platform
import docker
import psutil

version = '0.1.3.37'

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
    return (process_list)


def check_docker_state():
    try:
        run_dockers = docker.from_env()
        return True
    except Exception as e:
        return False


def get_docker_state():
    docker_state = []
    if not check_docker_state():
        docker_state.append(['Error connect to Docker !', '', '', ''])
        return docker_state
    else:
        run_dockers = docker.from_env()

        if len(run_dockers.containers.list()) == 0:
            docker_state.append(['Container(s) not found !', '', '', ''])
        else:
            for containerx in run_dockers.containers.list():
                docker_state.append([containerx, containerx.attrs['Name'], containerx.attrs['State']['Status'],
                                     containerx.attrs['Config']['Image']])
        return docker_state


def get_sys_info():
    sys_info_set = {}
    uname = platform.uname()
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    nodeip = str(conn.getresponse().read())
    dockerinfo = get_docker_state()
    system_time_stamp = datetime.now()
    memuse = psutil.virtual_memory()
    hddinfo = psutil.disk_partitions(False)
    sys_info_set.update({c_yellow + 'Section [SYSTEM]': '' + c_norm})
    sys_info_set.update({'Scrypt Name': 'LInux MOnitoring Node Scrypt'})
    sys_info_set.update({'Scrypt Version': version})
    sys_info_set.update({'Python Version': str(sys.version_info.major) + '.' + str(sys.version_info.minor)})
    sys_info_set.update({'Local time stamp': system_time_stamp.astimezone().strftime('%Y-%m-%d %H:%M:%S [%z]')})
    sys_info_set.update({'Version': uname.version})
    sys_info_set.update({'Release': uname.release })
    sys_info_set.update({'Node Name':uname.node })
    sys_info_set.update({'System': uname.system})
    sys_info_set.update({'Node IP': nodeip[2:-1]})
    sys_info_set.update({c_yellow + 'Section [CPU]': '' + c_norm})
    sys_info_set.update({'Processor': uname.processor})
    sys_info_set.update({'CPU_Core': str(psutil.cpu_count(logical=False))})
    sys_info_set.update({'CPU_Thread': str(psutil.cpu_count(logical=True))})
    sys_info_set.update({'CPU_Arch': os.getenv('PROCESSOR_ARCHITECTURE')})
    sys_info_set.update({'CPU_ID': str(os.getenv('PROCESSOR_IDENTIFIER'))})
    sys_info_set.update({'CPU_Level': str(os.getenv('PROCESSOR_LEVEL'))})
    sys_info_set.update({c_yellow + 'Section [MEM]': '' + c_norm})
    i = 0
    for key in memuse._fields:
        sys_info_set.update({'MEM ' + key :  memuse[i]})
        i = i + 1
    sys_info_set.update({c_yellow + 'Section [DISK]': '' + c_norm})
    for i in range(len(hddinfo)):
        s = str(hddinfo[i])
        sys_info_set.update({'Disk ' + str(i): s[10:-1:]})
    sys_info_set.update({c_yellow + 'Section [DOCKER]': '' + c_norm})
    i = 0
    for containerx in dockerinfo:
        sys_info_set.update({'Docker ' + str(i) : str(containerx[0]) + '  ' + str(containerx[1]) + '  ' + str(containerx[2]) + '  ' + str(containerx[3])})
        i = i +1

    return sys_info_set

def print_sys_info():
    info = get_sys_info()

    for key,val in info.items():
        print(key,' : ', val)

def get_time_end(start_time, durationtime='00:00'):
    temp_time = datetime.strptime(durationtime, '%H:%M').time()
    return start_time + timedelta(hours=temp_time.hour, minutes=temp_time.minute)


def get_local_time(noformated=False):
    if noformated:
        return datetime.now()
    else:
        return datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S [%z]')