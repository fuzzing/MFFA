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

import sys
import subprocess
import re
import time
from utils import *

if sys.argv[1] == '-h':
    print 'Usage:\n'
    print 'test.py <type> <audio/video> <play/noplay> <seed_number>\n'
    print 'type              - type of target (stagefright/sf2/stream/codec)'
    print 'audio             - seed files are of audio type'
    print 'video             - seed files are of video type'
    print 'play/noplay       - enable testing of playback capabilities'
    print 'seed_number       - number of the seed file to start from\n'
    print 'Ex: python test.py stagefright video noplay 0\n'
    sys.exit()

target_type = sys.argv[1]
format_type = sys.argv[2]
playback = sys.argv[3]
seed_number = sys.argv[4]

# get device ids

cmd = 'adb devices > devices.txt'
run_subproc(cmd)

# parse the device id file to get the device list

f1 = open('devices.txt', 'rw')
devices = f1.readlines()
count_devices = len(devices) - 2
dev = [None] * count_devices
c = 0
for i in range(1, len(devices) - 1):
    reg_device = re.compile('\S*\s')
    dev[c] = str(reg_device.findall(devices[i])[0])
    c = c + 1

# get batches list

f2 = open('batches.txt', 'rw')
batches = f2.readlines()
for i in range(0, len(batches)):
    batches[i] = batches[i].rstrip()

count_batches = len(batches)
if (count_batches == 0):
    print 'No batches to run'
    print 'Edit the batches.txt file!'
    sys.exit()

if count_batches < count_devices:
    print 'More devices than batches to run...'
    print '...quit now to use all available devices'
    time.sleep(5)
    print 'continuing...'

dev_batch = [str] * count_devices * count_batches
share = int(count_batches / count_devices)

batch_counter = 0
retcode1 = [None] * count_devices
retcode2 = [None] * count_devices

# flush the logcat buffer for each device before starting the campaign

for i in range(0, count_devices):
    cmd = 'adb -s ' + dev[i] + ' logcat -c'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

if target_type == 'stagefright':

    # each device must take their "share" from the total number of batches

    for x in range(1, share + 1):

        # give each device its batch for the current round

        for i in range(0, count_devices):

            # give batches[batch_counter] to dev[i] and increment batch_counter

            cmd = 'python sp_stagefright.py ' \
                + str(batches[batch_counter]) + ' ' + format_type \
                + ' ' + playback + ' ' + seed_number + ' ' \
                + dev[i]
            retcode1[i] = subprocess.Popen([cmd], shell=True)

            # start a log for the current device with its given batch

            cmd = 'adb -s ' + dev[i] + ' logcat -v time *:F > logs/' \
                + batches[batch_counter] + '_stagefright_' + str(dev[i])
            retcode2[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

        # wait for all devices to finish their round of batches

        for c in range(0, count_devices):
            retcode1[c].wait()
            print ' Device ' + str(c) + ' has finished round: ' + str(x)
        print '******* All devices have finished round: ' + str(x)

        # kill the logging processes for the current round

        cmd = 'kill -9 $(pgrep -f logcat)'
        run_subproc(cmd)

        # flush the logcat buffer for each device after each round

        for i in range(0, count_devices):
            flush_log(dev[i])

if target_type == 'codec':

    # each device must take their "share" from the total number of batches

    for x in range(1, share + 1):

        # give each device its batch for the current round

        for i in range(0, count_devices):

            # give batches[batch_counter] to dev[i] and increment batch_counter

            cmd = 'python sp_codec.py ' \
                  + str(batches[batch_counter]) + ' ' \
                  + format_type + ' ' + playback + ' ' \
                  + seed_number + ' ' + dev[i]
            retcode1[i] = subprocess.Popen([cmd], shell=True)

            # start a log for the current device with its given batch

            cmd = 'adb -s ' + dev[i] \
                  + ' logcat -v time *:F > logs/' \
                  + batches[batch_counter] + '_codec_' + dev[i]
            retcode2[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

        # wait for all devices to finish their round of batches

        for c in range(0, count_devices):
            retcode1[c].wait()
            print ' Device ' + str(c) + ' has finished round: ' + str(x)
        print '******* All devices have finished round: ' + str(x)

        # kill the logging processes for the current round

        cmd = 'kill -9 $(pgrep -f logcat)'
        run_subproc(cmd)

        # flush the logcat buffer for each device after each round

        for i in range(0, count_devices):
            flush_log(dev[i])

if target_type == 'sf2':

    # each device must take their "share" from the total number of batches

    for x in range(1, share + 1):

        # give each device its batch for the current round

        for i in range(0, count_devices):

            # give batches[batch_counter] to dev[i] and increment batch_counter

            cmd = 'python sp_sf2.py ' \
                  + str(batches[batch_counter]) \
                  + ' ' + format_type + ' ' + seed_number \
                  + ' ' + dev[i]
            retcode1[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

            # start a log for the current device with its given batch

            cmd = 'adb -s ' + dev[i] \
                  + ' logcat -v time *:F > logs/' \
                  + batches[batch_counter] + '_sf2_' \
                  + str(dev[i])
            retcode2[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

        # wait for all devices to finish their round of batches

        for c in range(0, count_devices):
            retcode1[c].wait()
            print ' Device ' + str(c) + ' has finished round: ' + str(x)
        print '******* All devices have finished round: ' + str(x)

        # kill the logging processes for the current round

        cmd = 'kill -9 $(pgrep -f logcat)'
        run_subproc(cmd)

        # flush the logcat buffer for each device after each round

        for i in range(0, count_devices):
            flush_log(dev[i])

if target_type == 'stream':

    # each device must take their "share" from the total number of batches

    for x in range(1, share + 1):

        # give each device its batch for the current round

        for i in range(0, count_devices):

            # give batches[batch_counter] to dev[i] and increment batch_counter

            cmd = 'python sp_stream.py ' \
                  + str(batches[batch_counter]) + ' ' \
                  + seed_number + ' ' + dev[i]
            retcode1[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

            # start a log for the current device with its given batch

            cmd = 'adb -s ' + dev[i] \
                  + ' logcat -v time *:F > logs/' \
                  + batches[batch_counter] + '_stream_' \
                  + str(dev[i])
            retcode2[i] = subprocess.Popen([cmd], shell=True)
            batch_counter = batch_counter + 1

        # wait for all devices to finish their round of batches

        for c in range(0, count_devices):
            retcode1[c].wait()
            print ' Device ' + str(c) + ' has finished round: ' + str(x)
        print '******* All devices have finished round: ' + str(x)

        # kill the logging processes for the current round

        cmd = 'kill -9 $(pgrep -f logcat)'
        run_subproc(cmd)

        # flush the logcat buffer for each device after each round

        for i in range(0, count_devices):
            flush_log(dev[i])
