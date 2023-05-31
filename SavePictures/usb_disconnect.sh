#!/bin/bash

project_dir=/home/pi/projects/FarmOnEdge-studies/SavePictures

unmount_device(){
    sudo umount $project_dir/usb
}

unmount_device