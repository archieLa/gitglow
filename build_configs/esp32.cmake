# ESP32 Platform Configuration for GitGlow
# This file is included by the main CMakeLists.txt when TARGET_PLATFORM=ESP32

message(STATUS "Configuring for ESP32 platform...")

# ESP-IDF integration
if(NOT DEFINED ENV{IDF_PATH})
    message(FATAL_ERROR "ESP-IDF environment not found. Please run: source $IDF_PATH/export.sh")
endif()

# Set ESP-IDF path
set(IDF_PATH $ENV{IDF_PATH})

# Include ESP-IDF CMake
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

# ESP32-specific source files
set(PLATFORM_SOURCES
    src/platforms/esp32/ESP32Platform.cpp
    src/platforms/esp32/ESP32MatrixWriter.cpp
    src/platforms/esp32/ESP32WiFiManager.cpp
    src/platforms/esp32/ESP32WebServer.cpp
    src/main_esp32.cpp
)

# ESP32-specific include directories
set(PLATFORM_INCLUDES
    src/platforms/esp32
)

# ESP32-specific libraries (will be handled by ESP-IDF)
set(PLATFORM_LIBRARIES
    # ESP-IDF components are automatically linked
)

# ESP32-specific compiler flags
set(PLATFORM_COMPILE_FLAGS
    -DTARGET_ESP32=1
    -DGITGLOW_PLATFORM="ESP32"
)

# ESP32-specific definitions
add_definitions(-DESP32_PLATFORM)

# ESP-IDF components
set(EXTRA_COMPONENT_DIRS
    components/led_strip
    components/wifi_manager
)

# ESP32 partition table (optional)
# set(PARTITION_TABLE_FILENAME "partitions.csv")

# ESP32 flash configuration
# set(CONFIG_ESPTOOLPY_FLASHMODE "dio")
# set(CONFIG_ESPTOOLPY_FLASHFREQ "40m")
# set(CONFIG_ESPTOOLPY_FLASHSIZE "4MB")

# Custom post-build function for ESP32
function(platform_post_build)
    message(STATUS "ESP32 post-build: Binary ready for flash")
endfunction()

message(STATUS "ESP32 configuration complete")