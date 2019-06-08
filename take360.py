#!/usr/bin/env python

import os
import io
import time
import sys
from skimage import io
import signal
import struct
import subprocess
import threading
import numpy as np
import argparse

################################################################
# Initialise the Raspberry Pi video
################################################################

################################################################
# Either run the following command before running the script:
#   sudo modprobe bcm2835-v4l2
# or add bcm2835-v4l2 to the /etc/modules file
################################################################

################################################################
# Image Parameters
################################################################

width = 2592
height = 1944
img_size = (width,height)

terminate = False                            

def signal_handling(signum,frame):           
    global terminate                         
    terminate = True  

###############################################################
class Take360(threading.Thread):
    def __init__(self, input_directory, start_delay, timelapse_enabled, timelapse_period, timelapse_seconds):
        self.input_directory = input_directory      # Directory in which to save images
        self.start_delay = start_delay              # Delay before taking pictures              
        self.timelapse_enabled = timelapse_enabled  # Enable the timelapse function
        self.timelapse_period = timelapse_period    # If timelapse enabled, the time gap between shots
        self.timelapse_seconds = timelapse_seconds  # If timelapse enabled, how long should it shoot for
        
        self._stop = threading.Event() 

        print("Take360 Capture Initialisation Complete")

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        print("Take360 Capture Starting")
        # keep looping infinitely until the thread is stopped
        
        print("Take360 Waiting for capture thread to start")
        time.sleep(self.start_delay)

        if self.timelapse_enabled:
            # Calculate the number of images
            image_count = int(self.timelapse_seconds / self.timelapse_period)

        # Image counter for naming the files
        counter = 0

        print("Take360 Starting Capture Loop")
        while True:
            try:
                if self.stopped(): 
                    return

                ################################################################
                # PiCamera wouldn't produce the full size image
                subprocess.run(["raspistill", "-3d", "sbs", "-o", self.input_directory+'{:07d}'.format(counter)+".jpg", "-w", str(width*2), "-h", str(height) ])
                print("Capture "+'{:07d}'.format(counter))
                counter += 1

                # If timelapse
                if self.timelapse_enabled:
                    # Has the timelapse finished
                    if counter >= image_count:
                        print("Capture completed")
                        print("Press Ctrl+c to exit.")
                        self.stop()
                    else:
                        time.sleep(self.timelapse_period)
                else:
                    # Exit the loop
                    self.stop()

            except KeyboardInterrupt as ki:
                print("Take360 Capture Exiting Loop")
                raise ki
            else:
                time.sleep(0)

    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet()  

################################################################

###############################################################
class Process360(threading.Thread):
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory    # Directory to look for images to process
        self.output_directory = output_directory  # directory to place processed images

        self._stop = threading.Event() 

        print("Take360 Process Loop Initialisation Complete")

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        print("Take360 Process Loop Starting")
        # keep looping infinitely until the thread is stopped

        while True:
            files = os.listdir(self.input_directory)

            try:
                if self.stopped(): 
                    return

                for file in files:
                    if file.endswith(".jpg"):
                        image = np.empty((height * width * 2 * 3), dtype=np.uint8)
                        image = io.imread(self.input_directory+file)

                        if image is not None:
                            image0 = image[0:height,0:width-1]
                            image1 = image[0:height,width:width*2-1]

                           # Create the tmp directory and save the images to it
                            if not os.path.isdir("./tmp/"):
                                os.mkdir("./tmp/")

                            io.imsave("./tmp/image0.jpg",image0)
                            io.imsave("./tmp/image1.jpg",image1)

                            # Create the hugin project file if it doesn't already exist
                            if not os.path.exists("project.pto"):
                                subprocess.run(["pto_gen", "--projection=2", "--fov=360", "-o", "project.pto", "./tmp/image0.jpg", "./tmp/image1.jpg" ])
                                subprocess.run(["pto_template", "--output=project.pto", "--template=stereopi-template.pto", "project.pto"])

                            # Process the images into a 360 degree panorama using hugin-tools
                            subprocess.run(["hugin_executor", "--stitching", "--prefix=output", "project.pto"])

                            # Move the output to the processed files folder and rename it
                            os.rename("output.jpg",self.output_directory+file) 
                            
                            # Clean up the tmp folder and delete it
                            os.remove("./tmp/image0.jpg")
                            os.remove("./tmp/image1.jpg")
                            os.rmdir("./tmp/")
                            
                            # The file is processed so move it to the processed folder
                            os.rename(self.input_directory+file,self.input_directory+"processed/"+file)

                            print("Take360 Process Loop waiting for file to process.")
                            print("Press Ctrl+c to exit.")
                            time.sleep(0)

            except KeyboardInterrupt as ki:
                print("Exiting Take360 Process Loop")
                raise ki
            else:
                time.sleep(0)

        return

    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet() 

################################################################

def main(args):
    if sys.version_info.major < 3 or (sys.version_info.major and sys.version_info.minor < 5):
        raise Exception("Must be using Python 3.5 or higher")
    
    # initialise

    # Capture CTRL+C
    signal.signal(signal.SIGINT,signal_handling) 

    # See if there's any command line arguments to process
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_dir', nargs=1, type=str, required=True, help='Directory to place shots into. Shots will be moved into a subfolder called processed after processing.')
    parser.add_argument('-o','--output_dir', nargs=1, type=str, required=True, help='Directory for processed images to be placed into.')
    parser.add_argument('-d','--start_delay', nargs=1, type=int, required=False, default=[0],  help='Delay before shooting starts.')
    parser.add_argument('-t','--timelapse', required=False, action='store_true', help='Enable timelapse mode.')
    parser.add_argument('-p','--period', nargs=1, type=int, required=False, default=[2], help='Seconds between shots (minimum of 2 seconds).')
    parser.add_argument('-s','--seconds', nargs=1, type=int, required=False, default=[0], help='Number of seconds to shoot timelapse.')
    parser.add_argument('--no_capture',  required=False, action='store_true', help='Capture images disabled. Can be disabled to run shooting and processing seperately.')
    parser.add_argument('--no_process', required=False, action='store_true', help='Process images disabled. Can be disabled to run shooting and processing seperately.')

    args = parser.parse_args()

    input_directory = args.input_dir[0]         # Directory to place shots into. Shots will be moved into a subfolder called processed after processing
    output_directory = args.output_dir[0]       # Directory for processed images to be placed into
    start_delay = int(args.start_delay[0])      # Delay before shooting starts
    timelapse_enabled = bool(args.timelapse)    # Enable timelapse mode
    timelapse_period = int(args.period[0])      # Seconds between shots
    timelapse_seconds = int(args.seconds[0])    # Number of seconds to shoot timelapse
    no_capture = bool(args.no_capture)          # Capture images enabled. Can be disabled to run shooting and processing seperately
    no_processing = bool(args.no_process)       # Process images enabled. Can be disabled to run shooting and processing seperately

    if timelapse_enabled:
        if timelapse_period >= timelapse_seconds:
            print("Timelpase period must be less than Timelapse seconds")
            os._exit(1)

    # Make sure the directory names en in /
    if not input_directory.endswith("/"):
        input_directory += "/"

    if not output_directory.endswith("/"):
        output_directory += "/"

    # Create any directories we need
    if not os.path.isdir(input_directory):
        os.mkdir(input_directory)
    
    if not os.path.isdir(input_directory+"processed/"):
        os.mkdir(input_directory+"processed/")

    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    if not no_processing:
        print("Start the processing thread")
        process = Process360(input_directory, output_directory).start()

    if not no_capture:
        print("Start the capture thread")
        capture = Take360(input_directory, start_delay, timelapse_enabled, timelapse_period, timelapse_seconds).start()

    # Terminate if CTRL+C pressed
    while not terminate:
        time.sleep(1)

    print("Stopping")
    if not no_capture:
        print("Closing Take360 Capture Loop")
        capture.stop()

    if not no_processing:
        print("Closing Take360 Process Loop")
        process.stop()

    print("Stopped")
    os._exit(0)

if __name__ == '__main__':
    main(sys.argv)
################################################################
