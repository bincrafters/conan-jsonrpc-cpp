project(test_package)
cmake_minimum_required(VERSION 3.1)

find_package(Threads REQUIRED)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB SOURCE_FILES *.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT})
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 11)
