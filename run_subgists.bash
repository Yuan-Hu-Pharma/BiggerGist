#!/bin/bash

##	Will run all gist.in commands in each subdirectory named SUB_*
##

for i in $(ls -d SUB_*);
do
	cd $i
	for j in $(ls *.in);
	do
		nohup cpptraj -i $j &
	done
	cd ../
done
