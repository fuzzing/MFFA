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
from utils import *

if sys.argv[1] == '-h':
    print 'Usage:\n'
    print 'sf2.py <path_seed_files> <audio/video/list> <seed_number> <device_id>'
    print 'path_seed_files   - path to directory containing the seed files'
    print 'audio             - seed files are of audio type'
    print 'video             - seed files are of video type'
    print 'seed_number       - number of the seed file to start from'
    print 'device_id         - device id\n'
    sys.exit()

seed_files = listdir(sys.argv[1])
root_path = sys.argv[1]
length = len(seed_files)
start = int(sys.argv[3])
device_id = sys.argv[4]

# flush logcat buffer if a new campaign is started

if start == 0:
    flush_log(device_id)

if sys.argv[2] == 'audio':
    for x in range(start, length):
        print '***** Sending file: ' + str(x) + ' - ' + seed_files[x]

        # push the file to the device

        cmd = 'adb -s ' + device_id + ' push ' + "'" + root_path \
            + '/' + seed_files[x] + "'" + " '/data/Music/" \
            + seed_files[x] + "'"
        run_subproc(cmd)

        # log the file being sent to the device

        cmd = 'adb -s ' + device_id \
            + " shell log -p F -t Stagefright - sp_sf2 '*** " + str(x) \
            + " - Filename:'" + seed_files[x]
        run_subproc(cmd)

        # try to decode audio file

        cmd = 'timeout 15 adb -s ' + device_id \
            + " shell sf2 -a '/data/Music/" + seed_files[x] + "'"
        run_subproc(cmd)

        # remove the file from the device

        cmd = 'adb -s ' + device_id + ' shell rm /data/Music/*'
        run_subproc(cmd)

if sys.argv[2] == 'video':
    for x in range(start, length):
        print '***** Sending file: ' + str(x) + ' - ' + seed_files[x]

        # push the file to the device

        cmd = 'adb -s ' + device_id + ' push ' + "'" + root_path \
            + '/' + seed_files[x] + "'" + " '/data/Movies/" \
            + seed_files[x] + "'"
        run_subproc(cmd)

        # log the file being sent to the device

        cmd = 'adb -s ' + device_id \
            + " shell log -p F -t Stagefright - sp_sf2 '*** " + str(x) \
            + " - Filename:'" + seed_files[x]
        run_subproc(cmd)

        # try to decode video

        cmd = 'timeout 15 adb -s ' + device_id \
            + " shell sf2 '/data/Movies/" + seed_files[x] + "'"
        run_subproc(cmd)

        # remove the file from the device

        cmd = 'adb -s ' + device_id + ' shell rm /data/Movies/*'
        run_subproc(cmd)
