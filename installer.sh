#!/bin/bash

#This installer downloads and installs the components required to preform automated commandline stitching on a Raspberry Pi. 

#Download and install Hugin Command Line Tools
echo -e "\e[1m\e[4mInstalling Hugin Command Line Tools\e[0m"
sudo apt-get --assume-yes install hugin-tools
echo "\e[1m\e[32mCompleted Hugin Tools install\e[0m"
echo ""
#Download and install enblend
echo -e "\e[1m\e[4mInstalling enblend\e[0m"
sudo apt-get --assume-yes install enblend
echo "\e[1m\e[32mCompleted enblend install\e[0m"
echo ""
#Download and install Eye of Gnome image viewer
echo -e "\e[1m\e[4mInstalling scikit-image\e[0m"
sudo apt-get --assume-yes install python3-skimage
echo "\e[1m\e[32mCompleted scikit-image install\e[0m"
echo ""
echo -e "\e[1m\e[4mChecking all installations for debuging puposes\e[0m"
hugin="$(dpkg -s hugin-tools | grep Status)"
echo -e "\e[1m\e[32mhugin-tools:\e[0m\e[33m\t${hugin}\e[0m"
enblend="$(dpkg -s enblend | grep Status)"
echo -e "\e[1m\e[32menblend:\e[0m\e[33m\t${enblend}\e[0m"
sklearn="$(dpkg -s python3-skimage | grep Status)"
echo -e "\e[1m\e[32mscikit-image:\e[0m\e[33m\t${sklearn}\e[0m"
echo ""
echo -e "\e[1m\e[4mMaking scripts executable\e[0m"
chmod +x *.sh
echo ""
echo -e "\e[1m\e[4m\e[32mInstall complete.\e[0m"
