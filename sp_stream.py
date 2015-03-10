#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
/*
 * Android media framework fuzzer
 * Copyright (c) 2015, Intel Corporation.
 * Author: Alexandru Blanda (ioan-alexandru.blanda@intel.com)
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

"""

from os import listdir
import sys
import subprocess
import re
import time

if sys.argv[1] == '-h':
    print '\nUsage:\n'
    print 'sp_stream.py <path_seed_files> <seed_number> <device_id>'
    print 'path_seed_files   - path to directory containing the seed files'
    print 'seed_number       - number of the seed file to start from'
    print 'device_id         - device id\n'
    sys.exit()

seed_files = listdir(sys.argv[1])
length = len(seed_files)
start = int(sys.argv[2])

# flush logcat buffer if a new campaign is started

if start == 0:
    r = subprocess.Popen(['adb -s ' + sys.argv[3] + ' logcat -c'],
                         shell=True)
    r.wait()

for x in range(start, length):
    print '***** Sending file: ' + str(x) + ' - ' + seed_files[x]

    # push the file to the device

    cmd = 'adb -s ' + sys.argv[3] + ' push ' + "'" + sys.argv[1] + '/' \
        + seed_files[x] + "'" + " '/data/Music/" + seed_files[x] + "'"
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

    # log the file being sent to the device

    cmd = 'adb -s ' + sys.argv[3] \
        + " shell log -p F -t Stagefright - sp_stream '*** " + str(x) \
        + " - Filename:'" + seed_files[x]
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

    # try to decode audio file

    cmd = 'timeout 15 adb -s ' + sys.argv[3] \
        + " shell stream '/data/Music/" + seed_files[x] + "'"
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

    # remove the file from the device

    cmd = 'adb -s ' + sys.argv[3] + ' shell rm /data/Music/*'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()
