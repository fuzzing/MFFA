# MFFA - Media Fuzzing Framework for Android

## Project overview

The main idea behind this project  is  to create corrupt  but structurally valid media files, direct them to the appropriate software components in Android to  be  decoded  and/or  played  and  monitor  the  system  for  potential  issues  (i.e  system crashes) that may lead to exploitable vulnerabilities. Custom developed Python scripts are used to send the malformed data across a distributed  infrastructure  of  Android  devices,  log  the  findings  and  monitor  for  possible issues, in an automated manner. The actual decoding of the media files on the Android devices is done using the Stagefright command line interface. The results  are sorted out, in an attempt to find only the unique issues, using a custom built triage mechanism.

### System and device configuration

The tool has been developed to be used inside a Linux environment. At the host system level, the only prerequisites are support for Python 2,7 or higher and the Android SDK.

For the device(s) under test the main problem is including the stagefright command line tool in the Android image that will be flashed on the device(s).

There are two alternatives for achieving this goal:

    if you are building an Android engineering image, you can directly modify 
the Android.mk file corresponding to the stagefright module. For that you need 
to go to frameworks/av/cmds/stagefright/ and edit the Android.mk file by looking
for the LOCAL_MODULE:=stagefright entry and modifying its corresponding 
LOCAL_MODULE_TAGS entry from optional to eng. Note that this will NOT work if 
you are trying to build an user or userdebug Android image:
    #LOCAL_MODULE_TAGS := optional
    LOCAL_MODULE_TAGS := eng
    LOCAL_MODULE:= stagefright

    the second alternative is to go to device/<vendor>/<target_product> and 
modify the device.mk file by adding the stagefright module to the 
PRODUCT_PACKAGES entry:
    PRODUCT_PACKAGES += \
        stagefright

### Tool configuration

Before starting the actual fuzzing campaign there are several configuration files that need to be taken care of:

    Firstly, you need to manually run adb devices > devices.txt to populate the devices.txt config file with the ids of the Android devices that will be used during testing
    Secondly, you need to write the batches.txt so that it contains the list of the directories containing the fuzzed input media files 
