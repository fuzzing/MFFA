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


def subprocess(cmd):
    r = subprocess.Popen([cmd], shell=True)
    r.wait()


"""
def subprocess_return(cmd):
    r = subprocess.Popen([cmd], shell=True)
    r.wait()

"""

def flush_log(device_id):
    cmd = 'adb -s ' + (str)(device_id) + ' logcat -c'
    r = subprocess.Popen([cmd], shell=True)
    r.wait()
