cmake_minimum_required(VERSION 3.16.3)
project(cpp_tasks)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.71.0 COMPONENTS regex numeric)

add_executable(cpp_tasks
#        task8/integralcalculator.cpp
#        task8/integralcalculator.h
        task7/ludecomposer.cpp task7/ludecomposer.h
#        task7/main.cpp
        task7/SquareMatrix.h task7/BlasBasedMatrix.h task7/BlasBasedMatrix.cpp
#        task7/jacobi.cpp
        task7/3digmat.cpp)

target_link_libraries (cpp_tasks "-pthread" "-lblas")
#target_compile_options(cpp_tasks PUBLIC "-pthread")
