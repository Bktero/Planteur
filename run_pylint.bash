#!/bin/bash
ls *.py | xargs -I file pylint file -rn