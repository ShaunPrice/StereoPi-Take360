# README

## Overview
This is an updated installation and example of the 360-Panorama example using the StereoPi (https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871).

This update was created to enable the software for the Raspbian Stretch OS on a Raspberry Pi Compute Module.

### Prerequisits
You need to have Python 3.5 or higher installed.

The application also requires the following that are installed by the *installer.sh* script if required.

	- hugin-tools
	- enblend
	- python3-skimage (scikit-image)

### Usage
Follow the StereoPi instructions at https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871.

Replace the stereopi-temlate.pto with the template you created using Hugin.

The command line format is:

	python3 take360.py -i indirecory -o outdirectory

	-i	--input_dir		required	Directory to place shots into. Shots will be moved into a subfolder called processed after processing.
    -o	--output_dir	required 	Directory for processed images to be placed into.
    -d	--start_delay				Delay before shooting starts (seconds).
    -t	--timelapse					Enable timelapse mode.
    -p	--period					Seconds between shots (minimum of 2 seconds).
    -s	--seconds					Number of seconds to shoot timelapse.
    --no_capture					Capture images disabled. Can be disabled to run shooting and processing seperately.
    --no_process					Process images disabled. Can be disabled to run shooting and processing seperately.

**Command examples:**

	Take a single panorama after 10 seconds:
		*python3 take360.py -i indirecory -o outdirectory -d 10*

	Take a timelapse for 20 seconds with an image taken every 2 seconds (this is the minuimum)
		*python3 take360.py -i indirecory -o outdirectory -timelapse -p 2 -s 20*

	Take a timelapse for 20 seconds with an image taken every 5 seconds but don't convert the stereo images into 360 panoramas.
		*python3 take360.py -i indirecory -o outdirectory --timelapse -p 5 -s 20 --no_capture*

	Only process the images. This can be usefull if you want to seperate the capture and conversion into a panorama.
		*python3 take360.py -i indirecory -o outdirectory --no_capture*

Further help and updates from https://github.com/ShaunPrice/StereoPi-Take360.

### TODO
	* PiCamera was the prefered library for communicating with the StereoPi's cameras but it would not work with the full resolution images. For this reason the script calls the raspistill utillity. This may be updated in future versions if it is corrected.

### Deprecated
	* The previous *take360.sh* bash script has been replaced with the *take360.py* python3 script.