#!/bin/bash
ls *.py | xargs -I pyfile pylint --rcfile="pylint.rc" -rn pyfile --disable="line-too-long"
