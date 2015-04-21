#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
/*
 * Android media framework fuzzer
 * Copyright (c) 2015, Intel Corporation.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 */

Author: Alexandru Blanda (ioan-alexandru.blanda@intel.com)
"""

import sys
import subprocess
import re
import time
from utils import *

if (sys.argv[1] == "-h"):
        print 'Usage:\n '
        print 'python triage.py <signal_type> <file_type>'
        print "signal_type   - {SIGSEGV, SIGABRT, SIGILL} (type of signal to catch)"
        print "file_type     - {video, audio} \n"
        sys.exit()

signal_type = sys.argv[1]
file_type = sys.argv[2]

#get device list
cmd = "adb devices > devices.txt"
subprocess(cmd)

f1 = open("devices.txt", "rw")
devices = f1.readlines()
count_devices = len(devices) - 2
dev = [None] * count_devices
c = 0
for i in range(1, len(devices)-1):
        reg_device = re.compile('\S*\s')
        dev[c] = (str)((reg_device.findall(devices[i]))[0])
        dev[c] = dev[c].rstrip()
        c = c + 1
count_devices = len(dev)

#get log list
f2 = open("logs.txt", "rw")
logs = f2.readlines()
for i in range(0, len(logs)):
        logs[i] = logs[i].rstrip()
count_logs = len(logs)

if (count_logs == 0):
    print 'No logs to run'
    print 'Edit the logs.txt file!'
    sys.exit()

if count_logs < count_devices:
    print 'More devices than logs to analyze...'
    print '...quit now to use all available devices'
    time.sleep(5)
    print 'continuing...'

retcode = [None] * count_devices

#each device must get a log to analyze
if (count_devices == count_logs):

        for i in range(0, count_devices):
            cmd = "python get_uniquecrash.py" + " " + logs[i] + " " + \
                  dev[i] + " " + file_type + " " + signal_type
            retcode[i] = subprocess.Popen([cmd], shell=True)

        #wait for each device to finish their logs
        for i in range(0, count_devices-1):
            retcode[i].wait()
else:
    print "Check number of logs and number of devices..."
