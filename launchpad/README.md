# LaunchPad: MSP430-EXP430G2

The MSP430-EXP430G2 board is the 'historical' LaunchPad development kit by Texas Instruments.

As stated on its [official page](http://www.ti.com/tool/msp-exp430g2) this demo board is not supported by [Code Composer Studio](http://www.ti.com/tool/ccstudio) on Mac and Linux.

As a Mac owner and a Linux lover I decided to try to setup an environment for Linux to develop software for this demo board inside a virtual machine (VirtualBox) running Xubuntu 16.04 LTS. Here is my journey and the lessons I have learned.



------
## Setting up an environment: the easy way

### Using official packages
My [first reading](https://mycontraption.com/programming-the-msp430-launchpad-on-ubuntu/) taught me that is was quite easy to get the needed tool to compile and program the board. You simply need to install a bunch of packages:

	$ sudo apt-get install binutils-msp430 gcc-msp430 msp430-libc mspdebug

You know have a `msp430-gcc` and `mspdebug` available from the command line.


### Where is msp430-gdb?!
Surprisingly there is no `msp430-gdb` coming with the above packages so you need to install an additional one, `msp430-gdb`:

	$ sudo apt install gdb-msp430


### Compile a program and debug it
Compile your program:

	$ msp430-gcc main.c -mmcu=msp430g2231

Start `mspdebug` as a gdb proxy:

	$ mspdebug rf2500 gdb

Run `msp430-gdb` and connect to the target:

	$ msp430-gdb a.out
	(gdb) target remote localhost:2000


### C++
If you want to compile a *.cpp file you should use `msp430-gcc` instead of `msp430-g++`. Indeed the later command automatically adds the option `-lstdc++` to the command line but it seems like there is no C++ library provided with the toolchain. The compilation consequently fails.

Note that the lack of a C++ library also means that standard header files such as  `<iostream>` or `<vector>` are not available.

### Limitations with these tools
The `msp430-gcc` version available from the Ubuntu repository is old:

	$ msp430-gcc --version
	msp430-gcc (GCC) 4.6.3 20120301 (mspgcc LTS 20120406 unpatched)
	Copyright (C) 2011 Free Software Foundation, Inc.
	This is free software; see the source for copying conditions.  There is NO
	warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

As a consequence `-std=c++11` is not supported and this seems quite fair for such an old toolchain.

I also encountered so issues with `mspdebug` going into infinite loop when trying to use `step` or `next` from gdb. The version provided by the package is also an old version:

	$ apt show mspdebug
	Package: mspdebug
	Version: 0.22-2
	[...]

The [release history from Github](https://github.com/dlbeer/mspdebug/releases) tells that version 0.22 was released in 2013. The latest version (as of December 2016) was released in May this year.



------
## Setting up an environment: the not so easy way (but the way to be more comfortable)

Facing these limitations and issues, I decided to move on to the newest versions.

### Manual Installation
Texas Instruments provides gcc toolchains for msp430 and msp432 MCUs on their [official website](http://www.ti.com/tool/msp430-gcc-opensource). The lastest version or msp430 MCUs can be downloaded from [this link](http://software-dl.ti.com/msp430/msp430_public_sw/mcu/msp430/MSPGCC/latest/index_FDS.html). On Linux, you will get `msp430-gcc-full-linux-installer-4.2.0.36.run`, you will give it the right to be executed with `chmod u+x` and you will run. A GUI installer appears and will guide you.

Once the installation is done, don't forget the `bin` folder to the `PATH`.

Note that this toolchain version doesn't support `#pragma VECTOR=` and you will have to use the attribute `__interrupt_vec()` instead.

Documentation can be found here:

* [MSP430 GCC User's Guide](http://www.ti.com/lit/ug/slau646b/slau646b.pdf)
* [GCC for MSP430™ Microcontrollers](http://www.ti.com/lit/ml/slau591c/slau591c.pdf)

The lastest version of `mspdebug` can be downloaded from the [project's GitHub page](https://github.com/dlbeer/mspdebug/releases).

If `usb.h` if not found when calling `make` to build the executable, then install `libusb`:

	$ sudo apt install libusb-dev


If `readline.h` is missing then build the following option:
	
	make WITHOUT_READLINE=1
	sudo make WITHOUT_READLINE=1 install


### CMake and Eclipse
I have discovered CMake in December 2016 and I have to say that I like it. I never got used to makefiles but I adopted CMake immediately... I am also  Eclipse-convinced so I generated an Eclipse project with CMake :

	cd [path to Eclipse workspace]
	mkdir mps430-project
	cd mps430-project
	cmake -G"Eclipse CDT4 - Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=msp430.cmake -DCMAKE_ECLIPSE_VERSION=4.5 [path to git repo]/Planteur/launchpad/

Finally, I imported this "existing project into workspace".

Note that I encountered the exact same problem described [here](http://stackoverflow.com/questions/37426334/eclipse-freezes-when-creating-a-new-project-or-a-new-class): Eclipse (Mars) froze when I tried to create a new class. Same problem, same solution: changing the version of GTK that Eclipse uses solved my issue.

It looks like I am not the only one to use Eclipse. See this (very complete article)[http://r6500.blogspot.fr/2014/11/portable-environment-for-msp430.html] by  Vicente Jiménez: "Portable environment for the MSP430 Launchpad".



------
## Writing a udev rule

If you don't want to run `mspdebug` through `sudo` all the time, you should set up a udev rule for the LaunchPad board. I didn't know how to do that so here are the notes I took while learning to do it.

First you can write these articles:
* [http://hackaday.com/2009/09/18/how-to-write-udev-rules/](http://hackaday.com/2009/09/18/how-to-write-udev-rules/)
* [http://reactivated.net/writing_udev_rules.html](http://reactivated.net/writing_udev_rules.html)

I followed the tutorial and proceeded as follow:

	$ tail -f /var/log/syslog
	
	[disconnect launchpad]
	
	Dec  9 07:31:53 pgradot-xubuntu kernel: [ 5808.698389] usb 1-1: USB disconnect, device number 6
	Dec  9 07:31:53 pgradot-xubuntu ModemManager[671]: <info>  (tty/ttyACM0): released by modem /sys/devices/pci0000:00/0000:00:06.0/usb1/1-1
	
	[reconnect launchpad]
	
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.008165] usb 1-1: new full-speed USB device number 7 using ohci-pci
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.321990] usb 1-1: New USB device found, idVendor=0451, idProduct=f432
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.321994] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.321995] usb 1-1: Product: Texas Instruments MSP-FET430UIF
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.321996] usb 1-1: Manufacturer: Texas Instruments
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.321998] usb 1-1: SerialNumber: 5DFF427A4D12263C
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.359831] cdc_acm 1-1:1.0: No union descriptor, testing for castrated device
	Dec  9 07:32:03 pgradot-xubuntu kernel: [ 5818.359848] cdc_acm 1-1:1.0: ttyACM0: USB ACM device
	Dec  9 07:32:13 pgradot-xubuntu kernel: [ 5828.445608] hid-generic 0003:0451:F432.0006: usb_submit_urb(ctrl) failed: -1
	Dec  9 07:32:13 pgradot-xubuntu kernel: [ 5828.446047] hid-generic 0003:0451:F432.0006: timeout initializing reports
	Dec  9 07:32:13 pgradot-xubuntu kernel: [ 5828.447490] hid-generic 0003:04
	
	
	$ udevadm info -q path -n /dev/ttyACM0
	/devices/pci0000:00/0000:00:06.0/usb1/1-1/1-1:1.0/tty/ttyACM0
	
	$ udevadm info -a -p $(!!)
	udevadm info -a -p $(udevadm info -q path -n /dev/ttyACM0)
	
	Udevadm info starts with the device specified by the devpath and then
	walks up the chain of parent devices. It prints for every device
	found, all possible attributes in the udev rules key format.
	A rule to match, can be composed by the attributes of the device
	and the attributes from one single parent device.
	
	  looking at device '/devices/pci0000:00/0000:00:06.0/usb1/1-1/1-1:1.0/tty/ttyACM0':
	    KERNEL=="ttyACM0"
	    SUBSYSTEM=="tty"
	    DRIVER==""
	
	  looking at parent device '/devices/pci0000:00/0000:00:06.0/usb1/1-1/1-1:1.0':
	    KERNELS=="1-1:1.0"
	    SUBSYSTEMS=="usb"
	    DRIVERS=="cdc_acm"
	    ATTRS{authorized}=="1"
	    ATTRS{bAlternateSetting}==" 0"
	    ATTRS{bInterfaceClass}=="02"
	    ATTRS{bInterfaceNumber}=="00"
	    ATTRS{bInterfaceProtocol}=="01"
	    ATTRS{bInterfaceSubClass}=="02"
	    ATTRS{bNumEndpoints}=="03"
	    ATTRS{bmCapabilities}=="2"
	    ATTRS{interface}=="MSP430 Application UART"
	    ATTRS{supports_autosuspend}=="1"
	
	  looking at parent device '/devices/pci0000:00/0000:00:06.0/usb1/1-1':
	    KERNELS=="1-1"
	    SUBSYSTEMS=="usb"
	    DRIVERS=="usb"
	    ATTRS{authorized}=="1"
	    ATTRS{avoid_reset_quirk}=="0"
	    ATTRS{bConfigurationValue}=="1"
	    ATTRS{bDeviceClass}=="00"
	    ATTRS{bDeviceProtocol}=="00"
	    ATTRS{bDeviceSubClass}=="00"
	    ATTRS{bMaxPacketSize0}=="8"
	    ATTRS{bMaxPower}=="100mA"
	    ATTRS{bNumConfigurations}=="1"
	    ATTRS{bNumInterfaces}==" 2"
	    ATTRS{bcdDevice}=="0100"
	    ATTRS{bmAttributes}=="80"
	    ATTRS{busnum}=="1"
	    ATTRS{configuration}==""
	    ATTRS{devnum}=="7"
	    ATTRS{devpath}=="1"
	    ATTRS{idProduct}=="f432"
	    ATTRS{idVendor}=="0451"
	    ATTRS{ltm_capable}=="no"
	    ATTRS{manufacturer}=="Texas Instruments"
	    ATTRS{maxchild}=="0"
	    ATTRS{product}=="Texas Instruments MSP-FET430UIF"
	    ATTRS{quirks}=="0x0"
	    ATTRS{removable}=="unknown"
	    ATTRS{serial}=="5DFF427A4D12263C"
	    ATTRS{speed}=="12"
	    ATTRS{urbnum}=="90"
	    ATTRS{version}==" 1.10"
	
	  looking at parent device '/devices/pci0000:00/0000:00:06.0/usb1':
	    KERNELS=="usb1"
	    SUBSYSTEMS=="usb"
	    DRIVERS=="usb"
	    ATTRS{authorized}=="1"
	    ATTRS{authorized_default}=="1"
	    ATTRS{avoid_reset_quirk}=="0"
	    ATTRS{bConfigurationValue}=="1"
	    ATTRS{bDeviceClass}=="09"
	    ATTRS{bDeviceProtocol}=="00"
	    ATTRS{bDeviceSubClass}=="00"
	    ATTRS{bMaxPacketSize0}=="64"
	    ATTRS{bMaxPower}=="0mA"
	    ATTRS{bNumConfigurations}=="1"
	    ATTRS{bNumInterfaces}==" 1"
	    ATTRS{bcdDevice}=="0404"
	    ATTRS{bmAttributes}=="e0"
	    ATTRS{busnum}=="1"
	    ATTRS{configuration}==""
	    ATTRS{devnum}=="1"
	    ATTRS{devpath}=="0"
	    ATTRS{idProduct}=="0001"
	    ATTRS{idVendor}=="1d6b"
	    ATTRS{interface_authorized_default}=="1"
	    ATTRS{ltm_capable}=="no"
	    ATTRS{manufacturer}=="Linux 4.4.0-51-generic ohci_hcd"
	    ATTRS{maxchild}=="12"
	    ATTRS{product}=="OHCI PCI host controller"
	    ATTRS{quirks}=="0x0"
	    ATTRS{removable}=="unknown"
	    ATTRS{serial}=="0000:00:06.0"
	    ATTRS{speed}=="12"
	    ATTRS{urbnum}=="190"
	    ATTRS{version}==" 1.10"
	
	  looking at parent device '/devices/pci0000:00/0000:00:06.0':
	    KERNELS=="0000:00:06.0"
	    SUBSYSTEMS=="pci"
	    DRIVERS=="ohci-pci"
	    ATTRS{broken_parity_status}=="0"
	    ATTRS{class}=="0x0c0310"
	    ATTRS{consistent_dma_mask_bits}=="32"
	    ATTRS{d3cold_allowed}=="0"
	    ATTRS{device}=="0x003f"
	    ATTRS{dma_mask_bits}=="32"
	    ATTRS{driver_override}=="(null)"
	    ATTRS{enable}=="1"
	    ATTRS{irq}=="11"
	    ATTRS{local_cpulist}=="0"
	    ATTRS{local_cpus}=="1"
	    ATTRS{msi_bus}=="1"
	    ATTRS{subsystem_device}=="0x0000"
	    ATTRS{subsystem_vendor}=="0x0000"
	    ATTRS{vendor}=="0x106b"
	
	  looking at parent device '/devices/pci0000:00':
	    KERNELS=="pci0000:00"
	    SUBSYSTEMS==""
	    DRIVERS==""

I had all the information I needed to write the udev rule:

	$ cd /etc/udev/rules.d/
	$ sudo gedit 42-ti-launchpad.rules
	[...]
	$ cat 42-ti-launchpad.rules 
	ATTRS{idVendor}=="0451", ATTRS{idProduct}=="f432", MODE="0666", GROUP="plugdev"
	$ sudo /etc/init.d/udev restart

Later, while writing udev rules for XBee dongles, I found out that often `lsusb` provides enough information to write the rule.



