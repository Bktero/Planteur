#!/bin/bash

if [[ $# -eq 0 ]]
then
	echo "No argument provided, use default filename 'a.out'"
	mspdebug rf2500 prog\ a.out
else
	echo "Using parameters passed to this script"
	mspdebug rf2500 prog\ $*
fi
