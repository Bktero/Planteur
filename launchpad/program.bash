#!/bin/bash

if [[ $# -eq 0 ]]
then
	echo "No argument provided, use default filename 'a.out'"
	sudo mspdebug rf2500 prog\ a.out
else
	echo "Using parameters passed to this script"
	sudo mspdebug rf2500 prog\ $*
fi
