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
import os
import sys
import subprocess
import re
import time


def audio_software(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -s -a '/data/Music/"
                               + seed_file + "'"], shell=True)
    retcode.wait()


def audio_hardware(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -r -a '/data/Music/"
                                + seed_file + "'"], shell=True)
    retcode.wait()


def playback_audio_software(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -s -a -o '/data/Music/"
                                + seed_file + "'"], shell=True)
    retcode.wait()


def playback_audio_hardware(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -r -a -o '/data/Music/"
                                + seed_file + "'"], shell=True)
    retcode.wait()


def video_software(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -s '/data/Movies/"
                               + seed_file + "'"], shell=True)
    retcode.wait()


def video_hardware(device, seed_file):
    retcode = subprocess.Popen(['timeout 15 adb -s ' + device
                               + " shell stagefright -r '/data/Movies/"
                               + seed_file + "'"], shell=True)
    retcode.wait()


if sys.argv[1] == '-h':
    print 'Usage:\n'
    print 'python stagefright.py <path_seed_files> <audio/video/list> <play/noplay> <seed_number> <device_id>\n'
    print 'path_seed_files   - path to directory containing the seed files'
    print 'list              - list decoder profiles and and components'
    print "audio             - seed files are of audio type"
    print 'video             - seed files are of video type'
    print "play/noplay       - enable testing of playback capabilities"
    print 'seed_number       - number of the seed file to start from'
    print 'device_id         - device id\n'
    sys.exit()

seed_files = listdir(sys.argv[1])
length = len(seed_files)
i = 0
start = int(sys.argv[4])

# flush logcat buffer if a new campaign is started

if start == 0:

    cmd = 'adb -s ' + sys.argv[5] + ' logcat -c'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

if sys.argv[2] == 'list':

    print 'Getting decoder profiles supported and listing components...\n'
    print '*** Decoder profiles: ***'
    cmd = 'adb -s ' + sys.argv[5] + ' shell stagefright -p'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

    print '*** Components: ***'
    cmd = 'adb -s ' + sys.argv[5] + ' shell stagefright -l'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

if sys.argv[2] == 'audio':
    for i in range(start, length):
        print '***** Sending file: ' + str(i) + ' - ' + seed_files[i]

        # push the file to the device

        cmd = 'adb -s ' + sys.argv[5] + ' push ' \
              + "'" + sys.argv[1] + '/' \
              + seed_files[i] + "'" \
              + " '/data/Music/" + seed_files[i]  \
              + "'"
        r = subprocess.Popen([cmd], shell=True)
        r.wait()

        # log the file being sent to the device

        cmd = 'adb -s ' + sys.argv[5] \
              + " shell log -p F -t Stagefright - sp_stagefright '***** " \
              + str(i) + " - Filename:'" + seed_files[i]
        r = subprocess.Popen([cmd], shell=True)
        r.wait()

        # try to decode audio file (use software codec)

        audio_software(sys.argv[5], seed_files[i])

        # try to decode audio file (use hardware codec)

        audio_hardware(sys.argv[5], seed_files[i])

        if sys.argv[3] == 'play':

            # try to play audio file (use software codec)

            playback_audio_software(sys.argv[5], seed_files[i])

            # try to play audio file (use hardware codec)

            playback_audio_hardware(sys.argv[5], seed_files[i])

        # remove the file from the device

        cmd = 'adb -s ' + sys.argv[5] \
              + ' shell rm /data/Music/*'
        r = subprocess.Popen([cmd], shell=True)
        r.wait()

if sys.argv[2] == 'video':
    for i in range(start, length):
        print '***** Sending file: ' + str(i) + ' - ' + seed_files[i]

        # push the file to the device

        cmd = 'adb -s ' + sys.argv[5] + ' push ' \
              + "'" + sys.argv[1] + '/' + seed_files[i] + "'" \
              + " '/data/Movies/" + seed_files[i] + "'"
        r = subprocess.Popen([cmd], shell=True)
        r.wait()

        # log the file being sent to the device

        cmd = 'adb -s ' + sys.argv[5] \
              + " shell log -p F -t Stagefright - sp_stagefright '*** " \
              + str(i) + " - Filename:'" + seed_files[i]
        r = subprocess.Popen([cmd], shell=True)
        r.wait()

        # try to decode video (use software codec)

        video_software(sys.argv[5], seed_files[i])

        # try to decode video (use hardware codec)

        video_hardware(sys.argv[5], seed_files[i])

        # remove the file from the device

        cmd = 'adb -s ' + sys.argv[5] + ' shell rm /data/Movies/*'
        r = subprocess.Popen([cmd], shell=True)
        r.wait()
