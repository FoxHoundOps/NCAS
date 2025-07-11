#!/bin/bash
# This script iterates through a directory (arg1) and looks for .pcap files to archive.
# If a zip file corresponding to the pcap is not found, the pcap is zipped
# @author: Damian Najera
# @version: 1.1
DIR="$1"

if [[ -d $DIR ]] # Check that first arg is valid path
then
    cd $DIR
    for d in */ ; do # Iterate through DIR
    	cd $d
    	for file in *; # Iterate through each file
    	do
    		# chmod, zip, chmod only if file is a PCAP and it does not already have a corresponding ZIP
    		if [[ $file == *.pcap ]] && [ ! -f "${file%.*}.zip" ]; then
		    	chmod 777 "$file" # Assign 777 permissions PCAP file
    			zip -9 "${file%.*}.zip" "$file" # Zip with optimal level of compression (9)
		     	chmod 777 "${file%.*}.zip" # Assign 777 permissions to new ZIP file
    		fi
		done
     	cd .. 
	done
else
    echo "Error: Invalid Path"
fi
