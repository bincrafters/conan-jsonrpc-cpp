cmake_minimum_required(VERSION 2.8.11)
project(jsonrpc-cpp CXX)

option(WITH_CURL "Build HTTP Client" OFF)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads REQUIRED)
if(WITH_CURL)
    find_package(CURL REQUIRED)
endif(WITH_CURL)

set(EXTRA_LIBS ${CMAKE_THREAD_LIBS_INIT})
if (WIN32)
    set(EXTRA_LIBS ${EXTRA_LIBS} ws2_32)
endif (WIN32)

set(SOURCE_DIR ${CMAKE_SOURCE_DIR}/source_subfolder/src)
set(HEADER_DIR ${CMAKE_SOURCE_DIR}/source_subfolder/include)

set(SOURCE_FILES ${SOURCE_DIR}/jsonrpc_handler.cpp
                 ${SOURCE_DIR}/jsonrpc_server.cpp
                 ${SOURCE_DIR}/jsonrpc_client.cpp
                 ${SOURCE_DIR}/jsonrpc_udpserver.cpp
                 ${SOURCE_DIR}/jsonrpc_tcpserver.cpp
                 ${SOURCE_DIR}/jsonrpc_udpclient.cpp
                 ${SOURCE_DIR}/jsonrpc_tcpclient.cpp
                 ${SOURCE_DIR}/netstring.cpp
                 ${SOURCE_DIR}/system.cpp
                 ${SOURCE_DIR}/networking.cpp)

set(HEADER_FILES ${HEADER_DIR}/jsonrpc.h
                 ${HEADER_DIR}/jsonrpc_handler.h
                 ${HEADER_DIR}/jsonrpc_server.h
                 ${HEADER_DIR}/jsonrpc_client.h
                 ${HEADER_DIR}/jsonrpc_udpserver.h
                 ${HEADER_DIR}/jsonrpc_tcpserver.h
                 ${HEADER_DIR}/jsonrpc_udpclient.h
                 ${HEADER_DIR}/jsonrpc_tcpclient.h
                 ${HEADER_DIR}/jsonrpc_common.h
                 ${HEADER_DIR}/netstring.h
                 ${HEADER_DIR}/system.h
                 ${HEADER_DIR}/networking.h)

if (CURL_FOUND)
    set(SOURCE_FILES ${SOURCE_FILES} ${SOURCE_DIR}/jsonrpc_httpclient.cpp)
    set(HEADER_FILES ${HEADER_FILES} ${HEADER_DIR}/jsonrpc_httpclient.h)
endif(CURL_FOUND)

add_library(${CMAKE_PROJECT_NAME} ${SOURCE_FILES} ${HEADER_FILES})
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE ${HEADER_DIR})
target_link_libraries(${CMAKE_PROJECT_NAME} PUBLIC ${CONAN_LIBS} ${EXTRA_LIBS})
if (CURL_FOUND)
    set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES COMPILE_FLAGS -DCURL_ENABLED)
endif(CURL_FOUND)

install(TARGETS ${CMAKE_PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
install(FILES ${HEADER_FILES} DESTINATION include)
