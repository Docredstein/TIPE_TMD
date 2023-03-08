# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "C:/pico/pico-sdk")

set(PICO_BOARD pico_w CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.4.0")
  message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.4.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

project(fw C CXX ASM)

set(PICO_CXX_ENABLE_EXCEPTIONS 1)

set(PICO_CXX_ENABLE_RTTI 1)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(fw fw.cpp hw_config.cpp)

pico_set_program_name(fw "fw")
pico_set_program_version(fw "0.1")

pico_enable_stdio_uart(fw 1)
pico_enable_stdio_usb(fw 0)

# Add the standard library to the build
target_link_libraries(fw
        pico_stdlib)

# Add the standard include files to the build
target_include_directories(fw PUBLIC
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/.. # for our common lwipopts or any other standard includes, if required
)
add_subdirectory(SD/FatFs_SPI build)

add_library(Motor_Control INTERFACE)
target_sources(Motor_Control INTERFACE
    Motor_Control.cpp)

add_library(logging INTERFACE)
target_sources(logging INTERFACE
        logging.cpp)
    
add_library(PID INTERFACE)
target_sources(PID INTERFACE
    PID.cpp)
add_library(LSM6DS3TR INTERFACE)
target_sources(LSM6DS3TR INTERFACE lsm6ds3tr-c_reg.c)
# Add any user requested libraries
target_link_libraries(fw
        Motor_Control
        PID
        logging
        FatFs_SPI
        LSM6DS3TR
        hardware_pwm
        hardware_spi
        hardware_i2c
        hardware_dma
        hardware_pio
        hardware_interp
        hardware_timer
        hardware_watchdog
        hardware_clocks
        pico_multicore
        pico_cyw43_arch_lwip_threadsafe_background
        )
pico_enable_stdio_usb(fw 1)
pico_enable_stdio_uart(fw 1)
pico_add_extra_outputs(fw)

