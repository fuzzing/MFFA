# MFFA - Media Fuzzing Framework for Android

## Project overview

The main idea behind this project  is  to create corrupt  but structurally valid media files, direct them to the appropriate software components in Android to  be  decoded  and/or  played  and  monitor  the  system  for  potential  issues  (i.e  system crashes) that may lead to exploitable vulnerabilities. Custom developed Python scripts are used to send the malformed data across a distributed  infrastructure  of  Android  devices,  log  the  findings  and  monitor  for  possible issues, in an automated manner. The actual decoding of the media files on the Android devices is done using the Stagefright command line interface. The results  are sorted out, in an attempt to find only the unique issues, using a custom built triage mechanism.
