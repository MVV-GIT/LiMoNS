#!/usr/bin/python3
# LInux MOnitoring Node Symbol scrypt
# LIMONS
# (c) DrCryptos / cryptocoins4all@gmail.com / @DrCryptos
# usr/local/limons

import argparse
import csv
import logging
import os
import sys
import time
from datetime import datetime

import lutil

args_namespace, duration, analyticsfile = None, None, None
flag_log, flag_analytic, flag_display, flag_docker_launched = False, False, False, False
mflag_cpu, mflag_mem, mflag_disk, mflag_network, mflag_docker = False, False, False, False, False

def out_analytics_init_header_cpu_percent (afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('CPU ID')

    for cpuinfoset in lutil.get_cpu_percent(False)._fields:
        adata.append(cpuinfoset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_cpu_times (afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('CPU ID')

    for cpuinfoset in lutil.get_cpu_times(False)._fields:
        adata.append(cpuinfoset)

    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_mem (afile):
    adata = []
    adata.append('DateTimeStamp')
    for memset in lutil.det_mem_full()._fields:
        adata.append(memset)
    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_disk_io_counters (afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('Disk ID')
    for diskset in lutil.get_disk_io_counters()._fields:
        adata.append(diskset)
    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_net_io_counters (afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('Interface')
    for netset in lutil.get_net_net_io_counters()._fields:
        adata.append(netset)
    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)


def out_analytics_init_header_docker (afile):
    adata = []
    adata.append('DateTimeStamp')
    adata.append('DockerName')
    adata.append('DockerContainer')
    adata.append('DockerState')
    adata.append('DockerImage')
    writer = csv.writer(afile, delimiter=';')
    writer.writerow(adata)





def out_analytics_data(dtimestamp, dmem, dcpuu, dcpuall, ddockerinfo, dmonitoring_time_start, fdisp=False,
                       fanalytics=False, afile=''):
    difftime = (dtimestamp - dmonitoring_time_start)

    if fdisp:
        os.system('cls' if os.name == 'nt' else 'clear')



    if fanalytics:




def monitor_thread(thmcount, thmonitoring_time_end, tanalyticsfile):
    iterations = 0
    while True:

        if ((thmcount > 0) and (iterations == thmcount)) or (
                (thmcount == 0) and (datetime.now() >= thmonitoring_time_end)):
            break

        try:
            iterations = iterations + 1
            monitoring_time_stamp = datetime.now()

            # Get info
            if mflag_cpu:
                pass

            if mflag_mem:
                pass

            if mflag_disk:
                pass

            if mflag_network:
                pass

            if mflag_docker:
                pass


                flag_log
                flag_analytic
                flag_display

            # mem = lutil.det_mem_full()
            # cpuu = int(lutil.get_cpu_percent_short(False))
            # cpuall = lutil.get_cpu_percent_short(True)
            # dockerinfo = None
            #
            # if flag_docker_launched:
            #     dockerinfo = lutil.get_docker_state()
            #
            # if flag_display:
            #     out_analytics_data(monitoring_time_stamp, dmem=mem, dcpuu=cpuu, dcpuall=cpuall, ddockerinfo=dockerinfo,
            #                        dmonitoring_time_start=monitoring_time_start, fdisp=True,
            #                        fanalytics=False, afile='')
            #
            # if flag_analytic:
            #     out_analytics_data(monitoring_time_stamp, dmem=mem, dcpuu=cpuu, dcpuall=cpuall, ddockerinfo=dockerinfo,
            #                        dmonitoring_time_start=monitoring_time_start, fdisp=False,
            #                        fanalytics=True, afile=tanalyticsfile)

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
        sys.exit(200)

    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-cpu', '--cpu',
        required=False,
        type=str,
        default='true',
        help='Observe CPU readings'
    )

    parser.add_argument(
        '-mem', '--mem',
        required=False,
        type=str,
        default='true',
        help='Observe MEM readings'
    )

    parser.add_argument(
        '-disk', '--disk',
        required=False,
        type=str,
        default='true',
        help='Observe DISK readings'
    )

    parser.add_argument(
        '-net', '--network',
        required=False,
        type=str,
        default='true',
        help='Observe NETWORK readings'
    )


    parser.add_argument(
        '-docker', '--docker',
        required=False,
        type=str,
        default='true',
        help='Observe DOCKER readings'
    )

    parser.add_argument(
        '-deb', '--debug',
        required=False,
        type=str,
        default='',
        help='Debug mode'
    )

    parser.add_argument(
        '-d', '--duration',
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
        default='True',
        help='Out data to logfile (default: true)'
    )

    parser.add_argument(
        '-analytics', '--analytics',
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

    flag_docker_launched = lutil.check_docker_state()



    if ((not flag_analytic) and (not flag_display)) or ((not mflag_cpu) and (not mflag_mem) and (not mflag_disk) and (not mflag_network) and (not mflag_docker)):
        exit(1000)


    if flag_log:
        logfilename = 'll' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
        logging.basicConfig(level=logging.INFO, filename=logfilename, format='%(asctime)s %(levelname)s:%(message)s')

    monitoring_time_end = None
    monitoring_time_start = datetime.now()

    if flag_analytic:
        file_name_timestamp = time.strftime("%Y%m%d-%H%M")

        if mflag_cpu:
            analyticsfilename_cpu_percent = 'lcpup-' + file_name_timestamp + '.csv'
            analyticsfile_cpu_percent = open(analyticsfilename_cpu_percent, 'w')
            out_analytics_init_header_cpu_percent(analyticsfile_cpu_percent)
            analyticsfile_cpu_percent.close()


            analyticsfilename_cpu_times = 'lcput-' + file_name_timestamp + '.csv'
            analyticsfile_cpu_times = open(analyticsfilename_cpu_times, 'w')
            out_analytics_init_header_cpu_times(analyticsfile_cpu_times)
            analyticsfile_cpu_times.close()


        if mflag_mem:
            analyticsfilename_mem = 'lmem-' + file_name_timestamp + '.csv'
            analyticsfile_mem = open(analyticsfilename_mem, 'w')
            out_analytics_init_header_mem(analyticsfile_mem)
            analyticsfile_mem.close()


        if mflag_disk:
            analyticsfilename_disk = 'ldisk-' + file_name_timestamp + '.csv'
            analyticsfile_disk = open(analyticsfilename_disk, 'w')
            out_analytics_init_header_disk(analyticsfile_disk)
            analyticsfile_disk.close()


        if mflag_network:
            analyticsfilename_net = 'lnet-' + file_name_timestamp + '.csv'
            analyticsfile_net = open(analyticsfilename_net, 'w')
            out_analytics_init_header_net(analyticsfile_net)
            analyticsfile_net.close()



        if mflag_docker:
            analyticsfilename_docker = 'ldocker-' + file_name_timestamp + '.csv'
            analyticsfile_docker = open(analyticsfilename_docker, 'w')
            out_analytics_init_header_docker(analyticsfile_docker)
            analyticsfile_docker.close()





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
