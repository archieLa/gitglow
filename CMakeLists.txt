# GitGlow - Multi-Platform LED Matrix Display
cmake_minimum_required(VERSION 3.16)

project(GitGlow 
    VERSION 1.0.0
    DESCRIPTION "GitHub Display"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build configuration
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Platform selection
if(NOT DEFINED TARGET_PLATFORM)
    message(FATAL_ERROR "TARGET_PLATFORM must be specified: ESP32 or RASPBERRY_PI")
endif()

# Add cmake modules path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

# Common source files
set(COMMON_SOURCES
    src/common/GitGlowApp.cpp
    src/common/GitHubAPI.cpp
    src/common/ContributionGraph.cpp
    src/common/WebServer.cpp
    src/common/ConfigManager.cpp
)

# Common include directories
set(COMMON_INCLUDES
    src/interfaces
    src/common
)

# Platform-specific configuration
if(TARGET_PLATFORM STREQUAL "ESP32")
    include(build_configs/esp32.cmake)
elseif(TARGET_PLATFORM STREQUAL "RASPBERRY_PI")
    include(build_configs/raspberry_pi.cmake)
else()
    message(FATAL_ERROR "Unsupported TARGET_PLATFORM: ${TARGET_PLATFORM}")
endif()

# Create main executable
add_executable(${PROJECT_NAME} ${COMMON_SOURCES} ${PLATFORM_SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${COMMON_INCLUDES} ${PLATFORM_INCLUDES})

# Link libraries
target_link_libraries(${PROJECT_NAME} ${PLATFORM_LIBRARIES})

# Compiler flags
target_compile_options(${PROJECT_NAME} PRIVATE ${PLATFORM_COMPILE_FLAGS})

# Platform-specific post-build steps
if(COMMAND platform_post_build)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E echo "Running platform-specific post-build steps..."
        COMMAND platform_post_build
    )
endif()

# Installation
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

# Development targets
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # Add debug flags
    target_compile_definitions(${PROJECT_NAME} PRIVATE GITGLOW_DEBUG=1)
    
    # Add testing if available
    option(ENABLE_TESTING "Enable testing" ON)
    if(ENABLE_TESTING)
        enable_testing()
        add_subdirectory(tests)
    endif()
endif()

# Print build information
message(STATUS "GitGlow Build Configuration:")
message(STATUS "  Platform: ${TARGET_PLATFORM}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Version: ${PROJECT_VERSION}")