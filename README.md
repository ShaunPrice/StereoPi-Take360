# README

## Overview
This is an updated installation and example of the 360-Panorama example using the StereoPi (https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871).

This update was created to enable the software for the Raspbian Stretch OS on a Raspberry Pi Compute Module.

### Usage
Follow the StereoPi instructions at https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871.

Replace the stereopi-temlate.pto with the template you created using Hugin.

The command line format is:

	./take360 [-p][-g][-r][-h]

	./take360         Create the panorama image as output.jpg.
	./take360 -p      Create the panorama image as output.jpg and preview the image.
	./take360 -g      Generate and save the project file for re-use in processing images.
	./take360 -r      Re-use the previously saved project file saved using the -s switch.to create the panorama image
	./take360 -g -r   Same as no option plus it saves the project file for re-use in processing images.
	./take360 -h      This help

This will capture the two images from the StereoPi's cameras and output the 360 degree panorama to:

	output.jpg

Further help and updates from https://github.com/ShaunPrice/StereoPi-Take360.