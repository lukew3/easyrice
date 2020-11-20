cmake_minimum_required(VERSION 2.8.9)
project(easyrice)

#Bring the headers, such as Student.h into the project
# Commented next line because I'm not using include at this time
#include_directories(include)

#Can manually add the sources using the set command as follows:
#set(SOURCES src/main.cpp src/Student.cpp)

#The file(GLOB...) allows for wildcard additions:
file(GLOB SOURCES "src/*.cpp")

add_executable(testEasyrice ${SOURCES})
