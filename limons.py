#!/usr/bin/python3
# LInux MOnitoring Node Symbol scrypt
# LIMONS
# (c) DrCryptos / cryptocoins4all@gmail.com / @DrCryptos
# usr/local/limons

import argparse
import os
import sys
import time

import lutil


def main():

        while True:

                time.sleep(timeout_between_querry)
                lutil.scr_set0(15)

                try:
                        print('[LI]nux [MO]nitoring [N]ode [S]ymbol = LIMONS v.[' + lutil.version + ']')
                        mem = lutil.det_mem_full
                        print('CPU % usage: ', lutil.get_cpu_percent_short(False))
                        print('MEM total = ', mem[0])
                        print('MEM available = ', mem[1])
                        print('MEM used % = ', mem[2])
                        print('MEM used = ', mem[3])
                        print('MEM free = ', mem[4])
                        print('=' * 40)

                        print('Docker state:')


                except Exception as e:
                        if str(args_namespace.log).lower() == 'true':
                                errlog.write('Error: [' + time.strftime("%Y%m%d-%H%M") + ']:' + '\n')
                                errlog.write(str(containerx), 'Name: [', containerx.attrs['Name'], '] Status: [',containerx.attrs['State']['Status'], ']' + '\n')
                                errlog.write('Exception code =' + str(e) + '\n')
                                errlog.write('=' * 80 + '\n')
                        print('Error !')
                        continue
        errlog.close()




if __name__ == "__main__":
        if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
                print('Requires Python 3.6 or above !')
                print('You have version ' + sys.version_info.major + '.' + ys.version_info.minor +' installed')
                sys.exit(1)

        os.system('cls' if os.name == 'nt' else 'clear')

        parser = argparse.ArgumentParser()

        parser.add_argument(
                '-p', '--pause',
                required=False,
                type=str,
                default=1000,
                help='Pause between requests msec. Defalt 1000 msec'
        )

        parser.add_argument(
                '-d', '--display',
                type=str,
                required=False,
                default='true',
                help='Out data on display (default: false or "0")'
        )

        parser.add_argument(
                '-l', '--log',
                type=str,
                required=False,
                default='true',
                help='Out data to logfile (default: false or "0")'
        )

        parser.add_argument(
                '-i', '--info',
                type=str,
                required=False,
                default='',
                help='Print resource info and stop (default: false or "0")'
        )

        parser.add_argument(
                '-v', '--version',
                required=False,
                type=str,
                default='',
                help='Print current version LeMoNS, and exit'
        )

        args_namespace = parser.parse_args()

        if str(args_namespace.version).lower() == 'true' or str(args_namespace.version).lower() == '1':
                lutil.sys_info(True, False)
                exit(0)


        timeout_between_querry = int(args_namespace.pause) / 1000

        if str(args_namespace.log).lower() == 'true':
                errlogfilename = 'limons2-' + time.strftime("%Y%m%d-%H%M") + '.log'
                syslogfilename = 'limons2-' + time.strftime("%Y%m%d-%H%M") + '.cvs'
                errlog = open(errlogfilename, 'w')
                syslog = open(syslogfilename, 'w')
                errlog.write('LInux MOnitoring Node Symbol scrypt. V.' + lutil.version + '\n')
                errlog.write('=' * 80 + '\n')

        main()