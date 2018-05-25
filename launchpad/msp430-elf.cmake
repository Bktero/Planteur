set(CMAKE_SYSTEM_NAME Generic)

# Set compilers
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
set(CMAKE_C_COMPILER msp430-elf-gcc)
set(CMAKE_CXX_COMPILER msp430-elf-g++)

# Problem when setting flags here: http://stackoverflow.com/questions/11423313/cmake-cross-compiling-c-flags-from-toolchain-file-ignored
# In addition, read http://stackoverflow.com/questions/23995019/what-is-the-modern-method-for-setting-general-compile-flags-in-cmake
# --> done in CMakeLists.txt

# Set path
set(CMAKE_FIND_ROOT_PATH /opt/ti/gcc/)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

include_directories("/opt/ti/gcc/include")
