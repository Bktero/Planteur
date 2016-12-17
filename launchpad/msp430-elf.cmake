set(CMAKE_SYSTEM_NAME Generic)

# Set compilers
set(CMAKE_C_COMPILER msp430-elf-gcc)
set(CMAKE_CXX_COMPILER msp430-elf-g++)

# Problem when setting flags here: http://stackoverflow.com/questions/11423313/cmake-cross-compiling-c-flags-from-toolchain-file-ignored
# In addition, read http://stackoverflow.com/questions/23995019/what-is-the-modern-method-for-setting-general-compile-flags-in-cmake
# --> done in CMakeLists.txt


# Set path
set(CMAKE_FIND_ROOT_PATH /usr/msp430/)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

include_directories("/usr/msp430/include")

