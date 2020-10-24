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


def out_analytics_init_header(afile, aallcpu, adockerinfo):
    if flag_analytic:

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

        if flag_docker_launched:
            dcount = len(adockerinfo)
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

        if flag_docker_launched:
            print('Docker state:')
            for docid in ddockerinfo:
                print(docid[0], ':', docid[1], ':', lutil.c_green if docid[2] == 'running' else lutil.c_red, docid[2],
                      lutil.c_norm, ':', docid[3])
        else:
            print('Docker/Container(s) not found in system')

    if fanalytics:
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

        if flag_docker_launched:
            for docid in ddockerinfo:
                adata.append(docid[0])
                adata.append(docid[1])
                adata.append(docid[2])
                adata.append(docid[3])

        writer = csv.writer(afile, delimiter=';')
        writer.writerow(adata)


def monitor_thread(thmcount, thmonitoring_time_end, tanalyticsfile):
    iterations = 0
    while True:

        if ((thmcount > 0) and (iterations == thmcount)) or (
                (thmcount == 0) and (datetime.now() >= thmonitoring_time_end)):
            break

        try:
            iterations = iterations + 1
            monitoring_time_stamp = datetime.now()
            mem = lutil.det_mem_full()
            cpuu = int(lutil.get_cpu_percent_short(False))
            cpuall = lutil.get_cpu_percent_short(True)
            dockerinfo = None

            if flag_docker_launched:
                dockerinfo = lutil.get_docker_state()

            if flag_display:
                out_analytics_data(monitoring_time_stamp, dmem=mem, dcpuu=cpuu, dcpuall=cpuall, ddockerinfo=dockerinfo,
                                   dmonitoring_time_start=monitoring_time_start, fdisp=True,
                                   fanalytics=False, afile='')

            if flag_analytic:
                out_analytics_data(monitoring_time_stamp, dmem=mem, dcpuu=cpuu, dcpuall=cpuall, ddockerinfo=dockerinfo,
                                   dmonitoring_time_start=monitoring_time_start, fdisp=False,
                                   fanalytics=True, afile=tanalyticsfile)

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
        '-e', '--debug',
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

    timeout_between_query = int(args_namespace.pause) / 1000

    flag_log = str(args_namespace.log).lower() == 'true'
    flag_analytic = str(args_namespace.analytics).lower() == 'true'
    flag_display = str(args_namespace.display).lower() == 'true'
    flag_debug = str(args_namespace.debug).lower() == 'true'
    flag_docker_launched = lutil.check_docker_state()
    duration = str(args_namespace.duration)

    if (not flag_analytic) and (not flag_display):
        exit(1000)

    if flag_log:
        logfilename = 'll' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.log'
        logging.basicConfig(level=logging.INFO, filename=logfilename, format='%(asctime)s %(levelname)s:%(message)s')

    monitoring_time_end = None
    monitoring_time_start = datetime.now()

    if flag_analytic:
        analyticsfilename = 'la-' + time.strftime("%Y%m%d-%H%M") + '.csv'
        analyticsfile = open(analyticsfilename, 'w')
        out_analytics_init_header(analyticsfile, lutil.get_cpu_percent_short(True), lutil.get_docker_state())

    mcount = 0
    monitoring_time_end = monitoring_time_start

    if duration == '00:00' or duration == None:
        mcount = 0
    else:
        if duration.isalnum():
            mcount = int(duration)
        else:
            monitoring_time_end = lutil.get_time_end(monitoring_time_start, args_namespace.duration)

    monitor_thread(mcount, monitoring_time_end, analyticsfile)
