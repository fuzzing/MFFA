# MFFA - Media Fuzzing Framework for Android (Stagefright fuzzer)

## Project overview

The main idea behind this project  is  to create corrupt  but structurally valid media files, direct them to the appropriate software components in Android to  be  decoded  and/or  played  and  monitor  the  system  for  potential  issues  (i.e  system crashes) that may lead to exploitable vulnerabilities. Custom developed Python scripts are used to send the malformed data across a distributed  infrastructure  of  Android  devices,  log  the  findings  and  monitor  for  possible issues, in an automated manner. The actual decoding of the media files on the Android devices is done using the Stagefright command line interface. The results  are sorted out, in an attempt to find only the unique issues, using a custom built triage mechanism.

### System and device configuration

The tool has been developed to be used inside a Linux environment. At the host system level, the only prerequisites are support for Python 2,7 or higher and the Android SDK.

For the device(s) under test the main problem is including the stagefright command line tool in the Android image that will be flashed on the device(s).

There are two alternatives for achieving this goal:

1. if you are building an Android engineering image, you can directly modify the Android.mk file corresponding to the stagefright module. For that you need to go to frameworks/av/cmds/stagefright/ and edit the Android.mk file by looking for the LOCAL_MODULE:=stagefright entry and modifying its corresponding LOCAL_MODULE_TAGS entry from optional to eng. Note that this will NOT work if you are trying to build an user or userdebug Android image.
```
    #LOCAL_MODULE_TAGS := optional
    LOCAL_MODULE_TAGS := eng
    LOCAL_MODULE:= stagefright
```
2. the second alternative is to go to device/<vendor>/<target_product> and modify the device.mk file by adding the stagefright module to the PRODUCT_PACKAGES entry
```
    PRODUCT_PACKAGES += \
        stagefright
```
### Tool configuration

Before starting the actual fuzzing campaign there are several configuration files that need to be taken care of:

1. Firstly, you need to manually run adb devices > devices.txt to populate the devices.txt config file with the ids of the Android devices that will be used during testing
2. Secondly, you need to write the batches.txt so that it contains the list of the directories containing the fuzzed input media files 

### Running a fuzzing campaign

Having configured these two files you can start the fuzzing campaign by issuing the following command:

```
 python test.py stagefright <video|audio> <play|noplay> <index>
    <video|audio> the media batches tested are audio or video files
    <play|noplay> in case of audio testing, try to also test the playback functionality of the framework or not
    <index>       in case you stop the fuzzing campaign at a certain index, you can restart from that certain point (for new campaigns use 0)
```

During the fuzzing process, a separate log will be created for each device in the testing infrastructure. The logs are updated real-time so you can check out partial results during the actual testing.

### Running a bug triage campaign

The triage mechanism will take the generated logs from the actual fuzzing phase, identify the crashing test cases, resend them to the devices, check if the issues have been encountered before and store the unique bugs. Before starting the actual triage process, you need to copy the generated logs to the root directory of the triage scripts. Also you need to populate the logs.txt config file with the file names of the logs, one per each line.

To start the triage process you need to issue the following command:

```

python triage.py <SIGSEGV|SIGILL|SIGFPE|all> <video|audio>
    <SIGSEGV|SIGILL|SIGFPE|all> - type of signal to look out for
    <video|audio>               - the media batches that were tested are audio or video files
```

### Some results

Multiple integer overflows in Stagefright code (libstagefright SampleTable):

CVE-2014-7915 

CVE-2014-7916 

CVE-2014-7917

A crafted MPEG4 media file can result in heap corruption in libstagefright, that can lead to arbitrary code execution in the mediaserver process.

CVE-2015-3832

### Papers, presentations

Android Builders Summit, March 2015 - http://events.linuxfoundation.org/sites/events/files/slides/ABS2015.pdf 

