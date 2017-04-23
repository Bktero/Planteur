#!/bin/bash

PLANTEUR_DIR=$(readlink -f "..")
VALIDATION_DIR=$(readlink -f ".")
WORKING_DIR=${VALIDATION_DIR}/working

function failure {
	echo "---------------------------------------"
	echo "**** Tests failed! ****"
	exit 1
}

function success {
	echo "---------------------------------------"
	echo "**** Test succeeded! ****"
}

function clean {
	echo "---------------------------------------"
	echo "**** Clean ****"

	if [ -f ${WORKING_DIR}/planteur.db ]
	then
		rm ${WORKING_DIR}/planteur.db
	fi

	if [ -f ${WORKING_DIR}/plants.json ]
	then
		rm ${WORKING_DIR}/plants.json
	fi
}

#-------------------------------------------------------
# XBee validation
#-------------------------------------------------------
function xbee_functionnal {
	# Generate launchpad executable
	make test_xbee.out

	# Configure Planteur for XBee
	cp ${VALIDATION_DIR}/xbee_plants.json plants.json

	# Run Planteur
	python3 app.py &
	PLANTEUR_PID=$!

	# Program launchpad
	echo "Program launchpad"
	mspdebug rf2500 prog\ test_xbee.out > /dev/null 2>&1

	# Wait a few seconds so that frames are received before stopping Planteur
	sleep 5
	echo "Stop Planteur"
	kill -9 ${PLANTEUR_PID}

	# Analyze results
	mv planteur.db xbee_planteur.db
	sqlite3 xbee_planteur.db 'select uid, humidity, temperature from monitoring;' > xbee_result.txt
	sqlite3 xbee_planteur.db 'select count(*) from watering;' >> xbee_result.txt

	diff ${VALIDATION_DIR}/xbee_expected.txt xbee_result.txt 

	if [ $? -eq 0 ]
	then
	    success
	else
	    failure
	fi
}

function xbee_robustness {
	# Generate launchpad executable
	make test_xbee_intense.out

	# Configure Planteur for XBee
	cp ${VALIDATION_DIR}/xbee_plants.json plants.json

	# Run Planteur
	python3 app.py &
	PLANTEUR_PID=$!

	# Program launchpad
	echo "Program launchpad"
	mspdebug rf2500 prog\ test_xbee_intense.out > /dev/null 2>&1

	# Wait a few seconds so that frames are received before stopping Planteur
	sleep 60
	echo "Stop Planteur"
	kill -9 ${PLANTEUR_PID}

	# Analyze results
	mv planteur.db xbee_planteur.db
	MONITORING=$(sqlite3 xbee_planteur.db 'select count(*) from monitoring;')
	WATERING=$(sqlite3 xbee_planteur.db 'select count(*) from watering;')

	echo ${MONITORING} ${WATERING}

	if [ ${MONITORING} -eq 4096 -a ${WATERING} -eq 2048 ]
	then
		success
	else
		failure
	fi
}


#-------------------------------------------------------
# Set up test environment
#-------------------------------------------------------

# Clear working directory
if [ -d ${WORKING_DIR} ]
then
	rm -rf ${WORKING_DIR}
fi
mkdir ${WORKING_DIR}

# Copy Planteur files into working directory
cp ${PLANTEUR_DIR}/*.py ${WORKING_DIR}

# Copy the config for tests into working directory
cp ${VALIDATION_DIR}/config.json ${WORKING_DIR}

# Enter working directory so that results files are created there
cd ${WORKING_DIR}

# Build CMake project
cmake -DCMAKE_TOOLCHAIN_FILE=msp430-elf.cmake ${PLANTEUR_DIR}/../launchpad

# Erase MCU's flash memory
make erase


#-------------------------------------------------------
# Run tests
#-------------------------------------------------------
xbee_functionnal
clean
xbee_robustness
clean






