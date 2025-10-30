# Raspberry Pi Platform Configuration for GitGlow
# This file is included by the main CMakeLists.txt when TARGET_PLATFORM=RASPBERRY_PI

message(STATUS "Configuring for Raspberry Pi platform...")

# Check for cross-compilation
if(CMAKE_CROSSCOMPILING)
    message(STATUS "Cross-compiling for Raspberry Pi")
else()
    message(STATUS "Native compilation on Raspberry Pi")
endif()

# Find required libraries for Raspberry Pi
find_package(PkgConfig REQUIRED)

# Find WS2812 library (rpi_ws281x)
find_library(WS281X_LIBRARY
    NAMES ws2811 rpi_ws281x
    PATHS /usr/local/lib /usr/lib
    DOC "WS2812 LED library for Raspberry Pi"
)

if(NOT WS281X_LIBRARY)
    message(WARNING "WS281X library not found. Will build without LED support.")
    set(WS281X_FOUND FALSE)
else()
    set(WS281X_FOUND TRUE)
    message(STATUS "Found WS281X library: ${WS281X_LIBRARY}")
endif()

# Find other required libraries
find_package(Threads REQUIRED)

# Check for GPIO access
find_path(PIGPIO_INCLUDE_DIR pigpio.h
    PATHS /usr/local/include /usr/include
)

find_library(PIGPIO_LIBRARY
    NAMES pigpio
    PATHS /usr/local/lib /usr/lib
)

if(PIGPIO_INCLUDE_DIR AND PIGPIO_LIBRARY)
    set(PIGPIO_FOUND TRUE)
    message(STATUS "Found pigpio library: ${PIGPIO_LIBRARY}")
else()
    set(PIGPIO_FOUND FALSE)
    message(WARNING "pigpio library not found. GPIO functionality may be limited.")
endif()

# Raspberry Pi specific source files
set(PLATFORM_SOURCES
    src/platforms/raspberry_pi/RaspberryPiPlatform.cpp
    src/platforms/raspberry_pi/RpiMatrixWriter.cpp
    src/platforms/raspberry_pi/RpiWiFiManager.cpp
    src/platforms/raspberry_pi/RpiWebServer.cpp
    src/main_rpi.cpp
)

# Raspberry Pi specific include directories
set(PLATFORM_INCLUDES
    src/platforms/raspberry_pi
)

# Raspberry Pi specific libraries
set(PLATFORM_LIBRARIES
    Threads::Threads
)

if(WS281X_FOUND)
    list(APPEND PLATFORM_LIBRARIES ${WS281X_LIBRARY})
    add_definitions(-DHAS_WS281X=1)
endif()

if(PIGPIO_FOUND)
    list(APPEND PLATFORM_LIBRARIES ${PIGPIO_LIBRARY})
    list(APPEND PLATFORM_INCLUDES ${PIGPIO_INCLUDE_DIR})
    add_definitions(-DHAS_PIGPIO=1)
endif()

# Raspberry Pi specific compiler flags
set(PLATFORM_COMPILE_FLAGS
    -DTARGET_RASPBERRY_PI=1
    -DGITGLOW_PLATFORM="RASPBERRY_PI"
    -pthread
)

# Raspberry Pi specific definitions
add_definitions(-DRASPBERRY_PI_PLATFORM)

# System-specific libraries for networking
find_package(PkgConfig REQUIRED)
pkg_check_modules(CURL REQUIRED libcurl)
if(CURL_FOUND)
    list(APPEND PLATFORM_LIBRARIES ${CURL_LIBRARIES})
    list(APPEND PLATFORM_INCLUDES ${CURL_INCLUDE_DIRS})
    add_definitions(-DHAS_CURL=1)
endif()

# Custom post-build function for Raspberry Pi
function(platform_post_build)
    message(STATUS "Raspberry Pi post-build: Setting executable permissions")
    # Set executable permissions
    execute_process(COMMAND chmod +x ${CMAKE_BINARY_DIR}/${PROJECT_NAME})
    
    # Create systemd service file
    configure_file(
        ${CMAKE_SOURCE_DIR}/scripts/gitglow.service.in
        ${CMAKE_BINARY_DIR}/gitglow.service
        @ONLY
    )
    
    message(STATUS "Systemd service file created: ${CMAKE_BINARY_DIR}/gitglow.service")
    message(STATUS "To install: sudo cp gitglow.service /etc/systemd/system/")
endfunction()

# Installation for Raspberry Pi
install(FILES ${CMAKE_BINARY_DIR}/gitglow.service
    DESTINATION /etc/systemd/system
    OPTIONAL
)

message(STATUS "Raspberry Pi configuration complete")