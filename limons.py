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
flag_log, flag_analytic, flag_display = False, False, False


def out_analytics_init_header(afile, aallcpu, adockerinfo):
    if flag_analytic:
        dcount = len(adockerinfo)
        adata = []
        adata.append('DateTimeStamp')
        adata.append('Process time')
        adata.append('CPU avr.usage %')

        for i in range(len(aallcpu)):
            adata.append('Core' + str(i) + '%')

        adata.append('MEM total')
        adata.append('MEM available')
        adata.append('MEM used %')
        adata.append('MEM used')
        adata.append('MEM free')
        for i in range(dcount):
            adata.append('DockerName' + str(i))
            adata.append('DockerContainer' + str(i))
            adata.append('DockerState' + str(i))
            adata.append('DockerImage' + str(i))
        writer = csv.writer(afile, delimiter=';')
        writer.writerow(adata)


def out_analytics_data(dtimestamp, dmem, dcpuu, dcpuall, ddockerinfo, dmonitoring_time_start, fdisp=False,
                       fanalytics=False, afile=''):
    difftime = (dtimestamp - dmonitoring_time_start)

    if fdisp:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('CPU avr.usage % = ', lutil.c_red if dcpuu > 75 else lutil.c_yellow if dcpuu > 50 else lutil.c_green,
              dcpuu, lutil.c_norm)
        for i in range(len(dcpuall)):
            print('Core ' + str(i) + ' usage %  = ',
                  lutil.c_red if dcpuall[i] > 75 else lutil.c_yellow if dcpuall[i] > 50 else lutil.c_green, dcpuall[i],
                  lutil.c_norm)
        print('MEM total = ', dmem[0])
        print('MEM available = ', dmem[1])
        print('MEM used % = ', lutil.c_red if dmem[2] > 75 else lutil.c_yellow if dmem[2] > 50 else lutil.c_green,
              dmem[2], lutil.c_norm)
        print('MEM used = ', dmem[3])
        print('MEM free = ', dmem[4])
        print('Time stamp = ', dtimestamp)
        print('Process time = ' + str(difftime))
        # print('=' * 60)
        print('Docker state:')
        for docid in ddockerinfo:
            print(docid[0], ':', docid[1], ':', lutil.c_green if docid[2] == 'running' else lutil.c_red, docid[2],
                  lutil.c_norm, ':', docid[3])

    if fanalytics:
        dcount = len(ddockerinfo)
        adata = []
        adata.append(dtimestamp)
        adata.append(difftime)
        adata.append(str(dcpuu).replace('.', ','))

        for i in range(len(dcpuall)):
            adata.append(str(dcpuall[i]).replace('.', ','))

        adata.append(dmem[0])
        adata.append(dmem[1])
        adata.append(dmem[2])
        adata.append(dmem[3])
        adata.append(dmem[4])

        for docid in ddockerinfo:
            adata.append(docid[0])
            adata.append(docid[1])
            adata.append(docid[2])
            adata.append(docid[3])

        writer = csv.writer(afile, delimiter=';')
        writer.writerow(adata)


def monitor_thread(thmcount, thmonitoring_time_end, tanalyticsfile):
    while (thmcount == True) or (datetime.now() <= thmonitoring_time_end):
        try:
            monitoring_time_stamp = datetime.now()
            mem = lutil.det_mem_full()
            cpuu = int(lutil.get_cpu_percent_short(False))
            cpuall = lutil.get_cpu_percent_short(True)

            dockerinfo = lutil.get_docker_state()

            if flag_display:
                out_analytics_data(monitoring_time_stamp, mem, cpuu, cpuall, dockerinfo, monitoring_time_start, True,
                                   False, afile='')

            if flag_analytic:
                out_analytics_data(monitoring_time_stamp, mem, cpuu, cpuall, dockerinfo, monitoring_time_start, False,
                                   True, afile=tanalyticsfile)

            time.sleep(timeout_between_querry)
        except Exception as e:
            if flag_log:
                logging.info('Error: [' + time.strftime("%Y%m%d-%H%M") + ']. Exception code =' + str(e) + '\n')
            if flag_display:
                print('Error !' + str(e))
            continue

    if flag_display:
        # print('=' * 60)
        print('\nExecution time: ' + lutil.c_green + str(datetime.now() - monitoring_time_start) + lutil.c_norm)
    exit(0)


if __name__ == "__main__":
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
        sys.exit(200)

    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser()

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
        '-od', '--display',
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
        '-oa', '--analytics',
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

    timeout_between_querry = int(args_namespace.pause) / 1000

    flag_log = str(args_namespace.log).lower() == 'true'
    flag_analytic = str(args_namespace.analytics).lower() == 'true'
    flag_display = str(args_namespace.display).lower() == 'true'
    duration = str(args_namespace.duration)

    if (flag_analytic != True) and (flag_display != True):
        exit(1000)

    if flag_log:
        logfilename = 'll' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
        logging.basicConfig(level=logging.INFO, filename=logfilename, format='%(asctime)s %(levelname)s:%(message)s')

    monitoring_time_end = None
    mcount = False
    monitoring_time_start = datetime.now()

    if flag_analytic:
        analyticsfilename = 'la-' + time.strftime("%Y%m%d-%H%M") + '.csv'
        analyticsfile = open(analyticsfilename, 'w')
        out_analytics_init_header(analyticsfile, lutil.get_cpu_percent_short(True), lutil.get_docker_state())

    if duration == '00:00' or duration == None:
        mcount = True
    else:
        monitoring_time_end = lutil.get_time_end(monitoring_time_start, args_namespace.duration)

    monitor_thread(mcount, monitoring_time_end, analyticsfile)
