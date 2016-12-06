# Launchpad

## Using C++

### Compiling in C++
Use msp430-gcc instead of msp430-g++. Indeed the later automatically adds -lstdc++ to the command line but no C++ library is provided with my toolchain. It means that #include files like <iostream> or <vector> are not available.

### C++ standard version
mspgcc version from Xubuntu packages is quite old:

$ msp430-gcc --version
msp430-gcc (GCC) 4.6.3 20120301 (mspgcc LTS 20120406 unpatched)
Copyright (C) 2011 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

-std=c++11 is not supported and it's seems quite fair for such an old toolchain. Should try to install a newer toolchain from TI's website. Maybe newer versions will also provide a C++ std library.
