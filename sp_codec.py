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
    print '\nUsage:\n'
    print 'codec.py <path_seed_files> <audio/video/list> <play/noplay> <seed_number> <device_id>'
    print 'path_seed_files     - path to directory containing the seed files'
    print 'audio               - seed files are of audio type'
    print 'video               - seed files are of video type'
    print 'play/noplay         - enable testing of playback capabilities'
    print 'seed_number         - number of the seed file to start from'
    print 'device_id           - device id\n'
    sys.exit()

seed_files = listdir(sys.argv[1])
root_path = sys.argv[1]
length = len(seed_files)
start = int(sys.argv[4])
device_id = sys.argv[5]

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
        subprocess(cmd)

       # log the file being sent to the device

        cmd = 'adb -s ' + device_id \
            + " shell log -p F -t Stagefright - sp_codec '*** " \
            + str(x) + " - Filename:'" + seed_files[x]
        subprocess(cmd)

       # try to decode audio file

        cmd = 'timeout 15 adb -s ' + device_id \
            + ' shell codec /data/Music/' + "'" + seed_files[x] + "'"
        subprocess(cmd)

        if sys.argv[3] == 'play':

            # try to play audio file
            cmd = 'timeout 15 adb -s ' + device_id \
                  + ' shell codec -o /data/Music/' + "'" + seed_files[x] + "'"
            subprocess(cmd)

       # remove the file from the device

        cmd = 'adb -s ' + device_id + ' shell rm /data/Music/*'
        subprocess(cmd)

if sys.argv[2] == 'video':
    for x in range(start, length):
        print '***** Sending file: ' + str(x) + ' - ' + seed_files[x]

        # push the file to the device

        cmd = 'adb -s ' + device_id + ' push ' + "'" + root_path \
            + '/' + seed_files[x] + "'" + " '/data/Movies/" \
            + seed_files[x] + "'"
        subprocess(cmd)

        # log the file being sent to the device

        cmd = 'adb -s ' + device_id \
            + " shell log -p F -t Stagefright - sp_codec '*** " \
            + str(x) + " - Filename:'" + seed_files[x]
        subprocess(cmd)

        # try to decode video and audio streams from video file

        cmd = 'timeout 15 adb -s ' + device_id \
            + ' shell codec /data/Movies/' + seed_files[x]
        subprocess(cmd)

        # remove the file from the device

        cmd = 'adb -s ' + device_id + ' shell rm /data/Movies/*'
        subprocess(cmd)
