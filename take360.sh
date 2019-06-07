#!/bin/bash

mkdir -p tmp

echo Capturing first picture
raspistill -cs 0 -o ./tmp/0.jpg

echo Capturing second picture
raspistill -cs 1 -o ./tmp/1.jpg

echo Processiong 360 degree Panorama
pto_gen --projection=2 --fov=360 -o ./tmp/project.pto ./tmp/0.jpg ./tmp/1.jpg
pto_template --output=./tmp/project.pto --template=stereopi-template.pto ./tmp/project.pto
hugin_executor --stitching --prefix=output ./tmp/project.pto

echo Cleaning up
rm -rf ./tmp

echo Diplaying 360 degree Panorama image
eog output.jpg
