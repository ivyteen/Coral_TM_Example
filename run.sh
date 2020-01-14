#!/bin/bash

export DISPLAY=:99

MOUNT_DIR="/media/pi"
LS_CMD="ls /dev/sd[a-g][1-9]"
XVFB_ARGS="-screen 0 1024x768x24 +extension GLX +render -noreset"
#CODE_PATH="/home/pi/edgetpu_example/teachable2.py"
MODEL_FILE_PATH="/media/pi/model_edgetpu.tflite"
RUN="/home/pi/Coral_TM_Example/teachable.py"
ERROR_IND="/home/pi/Coral_TM_Example/error_indicator.py"

function usbDiskMount() {
	local retval
	if mountpoint -q $MOUNT_DIR; then
		#echo "$MOUNT_DIR is already been mounted, start the code."
		retval=0
	else
		#echo "Not Mounted, Try to mount."
		declare -a LS_OUTPUT;
		LS_OUTPUT=($($LS_CMD))
		if [ ${#LS_OUTPUT[@]} -ne 1 ]; then
			#echo "Two or more USB disk is connected"
			#echo "Remain Only 1"
			# ERROR indication with LED
			retval=1
		else
		
			sudo mount ${LS_OUTPUT[0]} $MOUNT_DIR
			if [ $? -eq 0 ]; then
				#echo "Disk Mounted"
				retval=0
			else
				#echo "Disk not Mounted"
				retval=2
				# ERROR indication with LED
			fi
		fi
	fi

	#Check if the model file is in the disk
		
	if [ $retval -eq 0 -a ! -e $MODEL_FILE_PATH ]; then
		retval=3
	fi

	echo $retval
}

retval=$(usbDiskMount)

if [ $retval -eq 0 ]; then
	if pgrep Xvfb; then
		echo "Xvfb is already running"
	else
		echo "Xvfb start!"
		Xvfb $DISPLAY $XVFB_ARGS &
	#	$($XVFB_CMD) &
		if [ $? -eq 0 ]; then
			/usr/bin/python3 $RUN 
		fi
	fi
else
	echo $retval
	/usr/bin/python3 $ERROR_IND $retval
fi
