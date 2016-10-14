#!/bin/bash

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
	-dim|--griddim)
	DIM1="$2"
	DIM2="$3"
	DIM3="$4"
	shift
	;;
	-cntr|--gridcntr)
	CNT1="$2"
	CNT2="$3"
	CNT3="$4"
	shift
	;;
	-spacn|--gridspacn)
	SPACN="$2"
	shift
	;;
	-div|--division)
	DIV="$2"
	shift
	;;
esac
shift
done
echo GRIDDIM = "${DIM1},${DIM2},${DIM3}"
echo GRIDCNTR = "${CNT1},${CNT2},${CNT3}"
echo GRIDSPACN = "${SPACN}"
echo DIVISION = "${DIV}"




if !(($DIM1%$DIV)); then
	echo DIM1 divisible by DIV
	RANGEBOT=$(($CNT1-$DIM1))
	RANGETOP=$(($CNT1+$DIM1))
	DIM_2=$(($DIM1/2))
	DIM_4=$(($DIM1/4))
	echo RANGE =  "${RANGEBOT},${RANGETOP}"
	echo "${DIM_2}"
	echo "${DIM_4}"
	NEWDIM=$(($DIM_4+2))
	for i in `seq 1 $DIV`
	do
        	mkdir SUB_$i
        	NEWCNT[1]=$(($RANGEBOT+$DIM_4))
        	NEWCNT[2]=$(($CNT1-$DIM_4))
        	NEWCNT[3]=$(($CNT1+$DIM_4))
        	NEWCNT[4]=$(($RANGETOP-$DIM_4))
	done
	echo gist gridspacn "${SPACN}" gridcntr "${NEWCNT[1]} ${CNT2} ${CNT3}" griddim "${NEWDIM} ${DIM2} ${DIM3}" > SUB_1/gist1.in
        echo gist gridspacn "${SPACN}" gridcntr "${NEWCNT[2]} ${CNT2} ${CNT3}" griddim "${NEWDIM} ${DIM2} ${DIM3}" > SUB_2/gist2.in
        echo gist gridspacn "${SPACN}" gridcntr "${NEWCNT[3]} ${CNT2} ${CNT3}" griddim "${NEWDIM} ${DIM2} ${DIM3}" > SUB_3/gist3.in
        echo gist gridspacn "${SPACN}" gridcntr "${NEWCNT[4]} ${CNT2} ${CNT3}" griddim "${NEWDIM} ${DIM2} ${DIM3}" > SUB_4/gist4.in
elif !(($DIM2%$DIV)); then
	echo DIM2 divisible by DIV
	RANGEBOT=$(($CNT2-$DIM2))
        RANGETOP=$(($CNT2+$DIM2))
        DIM_2=$(($DIM2/2))
        DIM_4=$(($DIM2/4))
        echo RANGE =  "${RANGEBOT},${RANGETOP}"
        echo "${DIM_2}"
        echo "${DIM_4}"
        NEWDIM=$(($DIM_4+2))
        for i in `seq 1 $DIV`
        do
                mkdir SUB_$i
                NEWCNT[1]=$(($RANGEBOT+$DIM_4))
                NEWCNT[2]=$(($CNT2-$DIM_4))
                NEWCNT[3]=$(($CNT2+$DIM_4))
                NEWCNT[4]=$(($RANGETOP-$DIM_4))
        done
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${NEWCNT[1]} ${CNT3}" griddim "${DIM1} ${NEWDIM} ${DIM3}"
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${NEWCNT[2]} ${CNT3}" griddim "${DIM1} ${NEWDIM} ${DIM3}"  
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${NEWCNT[3]} ${CNT3}" griddim "${DIM1} ${NEWDIM} ${DIM3}"  
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${NEWCNT[4]} ${CNT3}" griddim "${DIM1} ${NEWDIM} ${DIM3}"  
elif !(($DIM3%$DIV)); then
	echo DIM3 divisible by DIV
	RANGEBOT=$(($CNT3-$DIM3))
        RANGETOP=$(($CNT3+$DIM3))
        DIM_2=$(($DIM3/2))
        DIM_4=$(($DIM3/4))
        echo RANGE =  "${RANGEBOT},${RANGETOP}"
        echo "${DIM_2}"
        echo "${DIM_4}"
        NEWDIM=$(($DIM_4+2))
        for i in `seq 1 $DIV`
        do
                mkdir SUB_$i
                NEWCNT[1]=$(($RANGEBOT+$DIM_4))
                NEWCNT[2]=$(($CNT3-$DIM_4))
                NEWCNT[3]=$(($CNT3+$DIM_4))
                NEWCNT[4]=$(($RANGETOP-$DIM_4))
        done
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${CNT2} ${NEWCNT[1]}" griddim "${DIM1} ${DIM2} ${NEWDIM}"
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${CNT2} ${NEWCNT[2]}" griddim "${DIM1} ${DIM2} ${NEWDIM}"  
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${CNT2} ${NEWCNT[3]}" griddim "${DIM1} ${DIM2} ${NEWDIM}"  
        echo gist gridspacn "${SPACN}" gridcntr "${CNT1} ${CNT2} ${NEWCNT[4]}" griddim "${DIM1} ${DIM2} ${NEWDIM}"  
else
	echo No dimensions divisible by DIV, close script
fi
