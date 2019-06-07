# README

## Overview
This is an updated installation and example of the 360-Panorama example using the StereoPi (https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871).

This update was created to enable the software for the Raspbian Stretch OS on a Raspberry Pi Compute Module.

### Usage
Follow the StereoPi instructions at https://medium.com/stereopi/stitching-360-panorama-with-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-by-step-guide-aeca3ff35871.

Replace the stereopi-temlate.pto with the template you created using Hugin.

The command line format is:

	./take360.sh

To previwe the image after it's processed use the -p switch:

	./take360.sh

This will capture the two images from the StereoPi's cameras and output the 360 degree panorama to:

	output.jpg