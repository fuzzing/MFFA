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
from os import listdir
import random
from utils import *

if sys.argv[1] == '-h':
    print 'Usage:\n '
    print 'get_uniquecrash.py <log_file> <device_id> <video/audio> <signal_type> '
    print 'log_file          - assigned log file name'
    print 'device_id         - id of targeted Android device'
    print 'video/audio       - type of test files'
    print 'signal_type       - {SIGSEGV/SIGABRT/SIGFPE/SIGILL} (type of signal to catch) \n'
    sys.exit()

log_file = sys.argv[1]
device_id = sys.argv[2]
file_type = sys.argv[3]
signal_type = sys.argv[4]
new_crashes = {}

#number of lines to go up in a log to look for a crashing testcase

log_density = 8

#regexp

regex_filename = re.compile("Filename:\S*")
regex_path = re.compile("\S*_stagefright")
regex_address = re.compile("pc\s\S*")

crash_count = 1

#get the full path to the filename that caused the crash

path = regex_path.findall(log_file)
path = (str)(path[0])
path = path.replace("_stagefright", "")
print "The path to the test files is: " + path

f = open(log_file, "r")
lines = f.readlines()

#parse every line of the current log

for count in range(0, len(lines)):
        if (signal_type in lines[count]): 
                check_no_lines = count - log_density
                if check_no_lines < 0:
                   diff = log_density - count 
                   check_no_lines = log_density - diff
                else:
                   check_no_lines = log_density
                for crash_line in range(1, check_no_lines):
                   if ("Filename:" in lines[count - crash_line]):
                       filename = regex_filename.findall(lines[count-crash_line])
                       filename = (str)(filename[0])
                       filename = filename[9:]
                       break                        

		#push the file to the device

		cmd = "adb -s " + device_id + " push " + path + "/" \
		      + filename + " /data/Music"
		run_subproc(cmd)

		#delete the contents of /data/tombstones from the device

		cmd = "adb -s " + device_id + " " + "shell rm /data/tombstones/*"
		run_subproc(cmd)

		#decode the file on the device

		if (file_type == "video"):
		    cmd = "timeout 15 adb -s " + device_id + " " \
		          + "shell stagefright /data/Music/" + filename
		    run_subproc(cmd)
		if (file_type == "audio"):
		    cmd = "timeout 15 adb -s " + device_id + " " \
		          + "shell stagefright -a /data/Music/" + filename
		    run_subproc(cmd)

		#remove the file from the device

		cmd = "adb -s " + device_id + " " + "shell rm /data/Music/*"
		run_subproc(cmd)

		#use a try-except construction
		#for cases when the file did not generate a tombstone
		#the issue is not reproducible

		try:

		    #grab the generated tombstone and rename it

		    tid = (str)(random.random())
		    tomb_name = "tombstone" + tid
		    cmd = "adb -s " + device_id + " pull " \
		          + " /data/tombstones/tombstone_00 " + tomb_name
		    run_subproc(cmd)

		    #parse the tombstone and check for the last accessed PC address

		    f = open(tomb_name, "r")
		    traces = f.readlines()
		    pc_check = 0
		    for x in range(0, len(traces)):
		        if ("backtrace" in traces[x]):

		            #get the pc address from the next line

		            pc_address = regex_address.findall(traces[x+1])
		            pc_address = (str)(pc_address[0])
		            pc_address = pc_address[3:]
		            print (str)(crash_count) + " -- PC address: " + pc_address
		            crash_count = crash_count + 1
		            pc_check = 1
		            break
		    if (pc_check == 0):
		        pc_address = "00000000"

		    #save the file as a new crash(or not) and log the findings

		    if (pc_address not in new_crashes.keys()):
		        new_crashes[pc_address] = filename
		        print "**NEW**" + pc_address

		        #create a new folder that will contain the tombstone
		        #and the file that generated the crash

		        cmd = "mkdir issues/" + pc_address
		        run_subproc(cmd)

		        #copy the tombstone in the new issue folder

		        cmd = "cp " + tomb_name + " issues/" + pc_address
		        run_subproc(cmd)

		        #save the file that caused the crash in the corresponding issue folder
		        #result: all the files that caused a crash are saved

		        cmd = "find -name " + filename
		        r = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
		        file_path = (str)(r.stdout.read())
		        file_path = file_path.rstrip()
		        r.wait()

		        cmd = "cp " + file_path + " issues/" + pc_address
		        run_subproc(cmd)

		    #delete the gathered tombstone

		    cmd = "rm " + tomb_name
		    run_subproc(cmd)
		    f.close()
		except IOError:
		    print "The file did not generate a tombstone..false positive"
		    continue

