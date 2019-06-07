#!/bin/bash

# Retrieve the command line options
argp="false"	# Preview
argc="true"		# Capture and process images
argg="false"	# Generate project file and save for re-use
argr="false"	# Re-use previously generated project file
argh="false"	# Help

project="./tmp/project.pto"

while getopts ":pgrh" opt
do
  case $opt in
    p ) argp="true"
		echo "Preview enabled"
    	;;
    g ) argg="true"
		echo "Generate and save project file only."
		project="project.pto"
    	;;
	r ) echo "Processiong image with previously generated project file."
		argr="true"
		project="project.pto"
    	;;
    h ) argc="false"	# Don't capture and process images
		echo "Usage:"
		echo "  ./take360 [-p][-g][-r][-h]"
		echo ""
		echo "  ./take360         Create the panorama image as output.jpg."
		echo "  ./take360 -p      Create the panorama image as output.jpg and preview"
		echo "                       the image."
		echo "  ./take360 -g      Generate and save the project file for re-use in"
		echo "                       processing images."
		echo "  ./take360 -r      Re-use the previously saved project file saved using"
		echo "                       the -s switch.to create the panorama image"
		echo "  ./take360 -g -r   Same as no option plus it saves the project file for"
		echo "                       re-use in processing images."
		echo "  ./take360 -h      This help"
		echo ""
		echo "Further help and updates from https://github.com/ShaunPrice/StereoPi-Take360"
    	;;
	\? ) echo "Processing images to 360 degree panorama."
		;;
  esac
done

if [ "$argc" = "true" ]
then
	echo "./take360 -h for help on the command line options."
	
	mkdir -p tmp

	echo "Capturing first picture"
	raspistill -cs 0 -o ./tmp/0.jpg

	echo "Capturing second picture"
	raspistill -cs 1 -o ./tmp/1.jpg
	echo "$project"
	pto_gen --projection=2 --fov=360 -o "$project" ./tmp/0.jpg ./tmp/1.jpg
    pto_template --output="$project" --template=stereopi-template.pto "$project"

	hugin_executor --stitching --prefix=output "$project"

	if [ "$argp" = "true" ]
	then
		echo "Diplaying 360 degree Panorama image"
		eog output.jpg
	fi

	echo "Cleaning up"
	rm -rf ./tmp
fi
