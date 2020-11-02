#!/usr/bin/python3
# LInux MOnitoring Node Scrypt
# LIMONS
# (c) DrCryptos / cryptocoins4all@gmail.com / @DrCryptos
# usr/local/limons
# limons.py -d 5 -p 1000 -analytics true -disp true -cpu true -mem true -disk true -net true -docker true

import argparse
import csv
import logging
import os
import sys
import time
from datetime import datetime

import psutil

import lutil

args_namespace, duration, analyticsfile = None, None, None
flag_log, flag_analytic, flag_display = False, False, False
mflag_cpu, mflag_mem, mflag_disk, mflag_network, mflag_docker = False, False, False, False, False


def out_analytics_init_header_cpu_total(afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('CPU ID')
    adata.append('CPU %')

    for cpuinfoset in psutil.cpu_times(False)._fields:
        adata.append(cpuinfoset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_mem(afile):
    adata = []
    adata.append('DateTimeStamp')

    for memset in psutil.virtual_memory()._fields:
        adata.append(memset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_disk_io_counters(afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('Disk ID')

    for diskset in psutil.disk_io_counters(False)._fields:
        adata.append(diskset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_net_io_counters(afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('Interface')

    for netset in psutil.net_io_counters(False)._fields:
        adata.append(netset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_docker(afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('DockerName')
    adata.append('DockerContainer')
    adata.append('DockerState')
    adata.append('DockerImage')
    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def section_cpu(monitoring_time_stamp=datetime.now()):
    if flag_display:
        print(lutil.c_cyan, '[CPU section]', lutil.c_norm, sep='')
    cpupercent = list(psutil.cpu_percent(percpu=True))
    cputime = list(psutil.cpu_times(percpu=True))
    for i in range(len(cpupercent)):
        if flag_analytic:
            writer = csv.writer(analyticsfile_cpu_percent, delimiter=';')
            adata = []
            adata.append(monitoring_time_stamp)
            adata.append(i)
            adata.append(str(cpupercent[i]).replace('.', ','))
            for cpuinfoset in cputime[i]:
                adata.append((str(cpuinfoset).replace('.', ',')))
            writer.writerow(adata)
        if flag_display:
            print('CPU ID:', i, 'Usage:',
                  lutil.c_red if cpupercent[i] >= 75 else lutil.c_yellow if cpupercent[i] >= 50 else lutil.c_green,
                  f"{cpupercent[i]:5.2f} %", lutil.c_norm, end='')
            j = 0
            for key in cputime[i]._fields:
                print(key + f" {cputime[i][j]:.4f}  ", end='')
                j = j + 1
            print()
    if flag_display:
        print()


def section_mem(monitoring_time_stamp=datetime.now()):
    if flag_display:
        print(lutil.c_cyan, '[MEM section]', lutil.c_norm, sep='')
    memuse = psutil.virtual_memory()
    if flag_analytic:
        writer = csv.writer(analyticsfile_mem, delimiter=';')
        adata = []
        adata.append(monitoring_time_stamp)
        for meminfo in memuse:
            adata.append(str(meminfo).replace('.', ','))
        writer.writerow(adata)

    if flag_display:
        print('MEM: ', end='')
        i = 0
        for key in memuse._fields:
            print(key, '=' if key != 'percent' else lutil.c_red if memuse[i] >= 75 else lutil.c_yellow if memuse[i] >= 50 else lutil.c_green,
                  memuse[i], '/', lutil.c_norm, end='')
            i = i + 1
        print('\n')


def section_disk(monitoring_time_stamp=datetime.now()):
    hdduse = psutil.disk_io_counters(True)
    if flag_display:
        print(lutil.c_cyan, '[DISK section]', lutil.c_norm, sep='')
    for hddname, hddsetmesure in hdduse.items():
        if flag_analytic:
            writer = csv.writer(analyticsfile_disk, delimiter=';')
            adata = []
            adata.append(monitoring_time_stamp)
            adata.append(hddname)
            for detail in hddsetmesure:
                adata.append(str(detail).replace('.', ','))
            writer.writerow(adata)
        if flag_display:
            print('Disk:', hddname, end='')
            i = 0
            for key in hddsetmesure._fields:
                print(' /', lutil.hddparamdict[key], '=', hddsetmesure[i], end='')
            print()
    if flag_display:
        print()


def section_net(monitoring_time_stamp=datetime.now()):
    netuse = psutil.net_io_counters(True)
    if flag_display:
        print(lutil.c_cyan, '[NET section]', lutil.c_norm, sep='')
    for netname, netsetmesure in netuse.items():
        if flag_analytic:
            writer = csv.writer(analyticsfile_net, delimiter=';')
            adata = []
            adata.append(monitoring_time_stamp)
            adata.append(netname)
            for detail in netsetmesure:
                adata.append(str(detail).replace('.', ','))
            writer.writerow(adata)
        if flag_display:
            print('Interface:', netname, end='')
            i = 0
            for key in netsetmesure._fields:
                print(' /', lutil.netparamdict[key], '=', netsetmesure[i], end='')
            print()
    if flag_display:
        print()


def section_docker(monitoring_time_stamp=datetime.now()):
    if flag_display:
        print(lutil.c_cyan, '[DOCKER section]', lutil.c_norm, sep='')
    if lutil.check_docker_state():
        dockeruse = lutil.get_docker_state()
        if flag_display:
            i = 0
            for containerx in dockeruse:
                print('Container ', i, ' : ', containerx[0], ' / ', containerx[1], ' / ', containerx[2], ' / ',
                      containerx[3])
                i = i + 1
            print()
        if flag_analytic:
            writer = csv.writer(analyticsfile_docker, delimiter=';')
            adata = []
            adata.append(monitoring_time_stamp)
            i = 0
            for containerx in dockeruse:
                adata.append('Docker ' + str(i))
                adata.append(containerx[0])
                adata.append(containerx[1])
                adata.append(containerx[2])
                adata.append(containerx[3])
                i = i + 1
            writer.writerow(adata)
    else:
        if flag_display:
            print('Running Docker not found...')
        if flag_analytic:
            writer = csv.writer(analyticsfile_docker, delimiter=';')
            adata = []
            adata.append(monitoring_time_stamp)
            adata.append('Dicker not found')
            writer.writerow(adata)


def monitor_thread(thmcount, thmonitoring_time_end):
    iterations = 0
    monitoring_time_start = datetime.now()

    while True:

        if ((thmcount > 0) and (iterations == thmcount)) or (
                (thmcount == 0) and (datetime.now() >= thmonitoring_time_end)):
            break

        try:
            iterations = iterations + 1
            # monitoring_time_stamp = datetime.now()
            if flag_display:
                os.system('cls' if os.name == 'nt' else 'clear')

            if mflag_cpu:
                section_cpu(datetime.now())
            if mflag_mem:
                section_mem(datetime.now())
            if mflag_disk:
                section_disk(datetime.now())
            if mflag_network:
                section_net(datetime.now())
            if mflag_docker:
                section_docker(datetime.now())

            time.sleep(timeout_between_query)

        except Exception as e:
            if flag_log:
                logging.info('Error: [' + time.strftime("%Y%m%d-%H%M") + ']. Exception code =' + str(e) + '\n')
            if flag_display:
                print('Error on monitor_thread !' + str(e))
            continue

    if flag_display:
        print('\nExecution time: ' + lutil.c_green + str(
            datetime.now() - monitoring_time_start) + lutil.c_norm + '. Iterations count = ' + str(iterations))

    exit(0)


if __name__ == "__main__":
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
        print('LiMoNS requires Python 3.6+ to run.')
        sys.exit(200)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-C','-cpu', '--cpu',
        required=False,
        type=str,
        default='false',
        help='Observe CPU readings'
    )

    parser.add_argument(
        '-M','-mem', '--mem',
        required=False,
        type=str,
        default='false',
        help='Observe MEM readings'
    )

    parser.add_argument(
        '-disk', '--disk',
        required=False,
        type=str,
        default='false',
        help='Observe DISK readings'
    )

    parser.add_argument(
        '-N','-net', '--network',
        required=False,
        type=str,
        default='false',
        help='Observe NETWORK readings'
    )

    parser.add_argument(
        '-doc', '--docker',
        required=False,
        type=str,
        default='false',
        help='Observe DOCKER readings'
    )

    parser.add_argument(
        '-deb', '--debug',
        required=False,
        type=str,
        default='false',
        help='Debug mode'
    )

    parser.add_argument(
        '-D','-d', '--duration',
        required=True,
        type=str,
        default='00:00',
        help='Monitoring duration (HH:MM), 00:00 not limit'
    )

    parser.add_argument(
        '-p', '--pause',
        required=False,
        type=str,
        default=1000,
        help='Delay between requests msec. Defalt 1000 msec'
    )

    parser.add_argument(
        '-disp', '--display',
        type=str,
        required=False,
        default='false',
        help='Out data on display (default: false)'
    )

    parser.add_argument(
        '-l', '--log',
        type=str,
        required=False,
        default='false',
        help='Out data to logfile (default: true)'
    )

    parser.add_argument(
        '-A','-analytics', '--analytics',
        type=str,
        required=False,
        default='False',
        help='Save analytic data (default: false)'
    )

    parser.add_argument(
        '-v', '--version',
        required=False,
        type=str,
        default='',
        help='Print current version LeMoNS, and exit'
    )

    args_namespace = parser.parse_args()


    if str(args_namespace.version).lower() == '?':
        lutil.print_sys_info()
        exit(0)

    mflag_cpu = str(args_namespace.cpu).lower() == 'true'
    mflag_mem = str(args_namespace.mem).lower() == 'true'
    mflag_disk = str(args_namespace.disk).lower() == 'true'
    mflag_network = str(args_namespace.network).lower() == 'true'
    mflag_docker = str(args_namespace.docker).lower() == 'true'

    timeout_between_query = int(args_namespace.pause) / 1000
    duration = str(args_namespace.duration)

    flag_log = str(args_namespace.log).lower() == 'true'
    flag_analytic = str(args_namespace.analytics).lower() == 'true'
    flag_display = str(args_namespace.display).lower() == 'true'
    flag_debug = str(args_namespace.debug).lower() == 'true'

    if ((not flag_analytic) and (not flag_display)) or (
            (not mflag_cpu) and (not mflag_mem) and (not mflag_disk) and (not mflag_network) and (not mflag_docker)):
        exit(1000)

    if flag_log:
        logfilename = 'limons' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
        logging.basicConfig(level=logging.INFO, filename=logfilename, format='%(asctime)s %(levelname)s:%(message)s')

    monitoring_time_end = None
    monitoring_time_start = datetime.now()

    if flag_analytic:
        file_name_timestamp = time.strftime("%Y%m%d-%H%M")

        if mflag_cpu:
            analyticsfilename_cpu_percent = 'l-cpu-' + file_name_timestamp + '.csv'
            analyticsfile_cpu_percent = open(analyticsfilename_cpu_percent, 'w')
            out_analytics_init_header_cpu_total(analyticsfile_cpu_percent)

        if mflag_mem:
            analyticsfilename_mem = 'l-mem-' + file_name_timestamp + '.csv'
            analyticsfile_mem = open(analyticsfilename_mem, 'w')
            out_analytics_init_header_mem(analyticsfile_mem)

        if mflag_disk:
            analyticsfilename_disk = 'l-disk-' + file_name_timestamp + '.csv'
            analyticsfile_disk = open(analyticsfilename_disk, 'w')
            out_analytics_init_header_disk_io_counters(analyticsfile_disk)

        if mflag_network:
            analyticsfilename_net = 'l-net-' + file_name_timestamp + '.csv'
            analyticsfile_net = open(analyticsfilename_net, 'w')
            out_analytics_init_header_net_io_counters(analyticsfile_net)

        if mflag_docker:
            analyticsfilename_docker = 'l-docker-' + file_name_timestamp + '.csv'
            analyticsfile_docker = open(analyticsfilename_docker, 'w')
            out_analytics_init_header_docker(analyticsfile_docker)

    mcount = 0
    monitoring_time_end = monitoring_time_start

    if duration == '00:00' or duration == None:
        mcount = 0
    else:
        if duration.isalnum():
            mcount = int(duration)
        else:
            monitoring_time_end = lutil.get_time_end(monitoring_time_start, args_namespace.duration)

    monitor_thread(mcount, monitoring_time_end)

    if mflag_cpu:
        analyticsfile_cpu_percent.close()
    if mflag_mem:
        analyticsfile_mem.close()
    if mflag_disk:
        analyticsfile_disk.close()
    if mflag_network:
        analyticsfile_net.close()
    if mflag_docker:
        analyticsfile_docker.close()
