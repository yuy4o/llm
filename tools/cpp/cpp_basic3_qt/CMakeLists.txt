cmake_minimum_required(VERSION 3.5)

project(cpp_basic3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(cpp_basic3 main.cpp)

install(TARGETS cpp_basic3
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})
