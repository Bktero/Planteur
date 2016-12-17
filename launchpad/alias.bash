#!/bin/bash

alias gdb_proxy='sudo mspdebug rf2500 gdb 1>/dev/null 2>&1 &'
alias gdb_client='msp430-elf-gdb a.out --command=../command.gdb --quiet'

alias debug='gdb_proxy gdb_client' # no separator between commands because the first ends with & (run in background)
alias erase='mspdebug ; rf2500 erase'

alias program="mspdebug rf2500 'prog a.out'"
