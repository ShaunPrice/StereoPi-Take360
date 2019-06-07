#!/bin/bash

#This installer downloads and installs the components required to preform automated commandline stitching on a Raspberry Pi. 

#Download and install Hugin Command Line Tools
echo "Installing Hugin Command Line Tools"
sudo apt-get install hugin-tools
echo "Completed Hugin Tools install" #This doesn't actually check if the installation was successful, so it is possible for the install to fail but this message to still appear. 

#Download and install enblend
echo "Installing enblend"
sudo apt-get install enblend
echo "Completed enblend install"  #This doesn't actually check if the installation was successful, so it is possible for the install to fail but this message to still appear. 

#Download and install Eye of Gnome image viewer
echo "Installing enblend"
sudo apt-get install enblend
echo "Completed enblend install"  #This doesn't actually check if the installation was successful, so it is possible for the install to fail but this message to still appear. 

# Making scripts executable
chmod +x *.sh

echo "Install complete."

echo "run ./take360.sh"