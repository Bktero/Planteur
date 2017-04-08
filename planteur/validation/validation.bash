#!/bin/bash

function failure {
	echo "---------------------------------------"
	echo "Tests failed!"
	exit 1
}

function success {
	echo "---------------------------------------"
	echo "Tests succeeded!"
	exit 0
}



#-------------------------------------------------------
# Set up test environment
#-------------------------------------------------------
PLANTEUR_DIR=$(readlink -f "..")
VALIDATION_DIR=$(readlink -f ".")
WORKING_DIR=${VALIDATION_DIR}/working

echo PLANTEUR_DIR=${PLANTEUR_DIR}
echo VALIDATION_DIR=${VALIDATION_DIR}
echo WORKING_DIR=${WORKING_DIR}

# Clear and create working directory
rm -rf ${WORKING_DIR}
mkdir ${WORKING_DIR}

# Copy Planteur files into working directory
cp ${PLANTEUR_DIR}/*.py ${WORKING_DIR}
cp ${PLANTEUR_DIR}/config.json ${WORKING_DIR}

# Enter working directory so that results files are created there
cd ${WORKING_DIR}



#-------------------------------------------------------
# XBee validation
#-------------------------------------------------------
# Generate launchpad executable
cmake -DCMAKE_TOOLCHAIN_FILE=msp430-elf.cmake ${PLANTEUR_DIR}/../launchpad
make test_xbee.out

# Configure planteur for XBee
cp ${VALIDATION_DIR}/xbee_plants.json plants.json

# Run Planteur
python3 app.py &
PLANTEUR_PID=$!

# Program launchpad
echo "Program launchpad"
mspdebug rf2500 prog\ test_xbee.out > /dev/null 2>&1

# Wait a few second so that frames are exchanged being stoping Planteur
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
