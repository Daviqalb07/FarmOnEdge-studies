#!/bin/bash

project_dir=/home/pi/projects/FarmOnEdge-studies/SavePictures
images_dir=$project_dir/images
device=$1

mount_device(){
    mount $device $project_dir/usb
}

upload_images_to_device(){
    mv $1/* $project_dir/usb/images
}

mount_device
if [ "$(ls -A $images_dir)" ]; then
    upload_images_to_device images_dir
fi