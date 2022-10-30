cmake_minimum_required(VERSION 3.6)

set(CMAKE_CXX_STANDARD 14)

project("H5DataGen" VERSION 0.1)
find_package(HDF5 REQUIRED)


include(CMakePackageConfigHelpers)

add_custom_target(HeaderGen
                  COMMAND ./transform.py -o test/build -I test/inc -I test/inc/test2 test/inc/test.h
                  COMMAND ./transform.py -o test/build -I test/inc -I test/inc/test2 test/inc/test2/test2.h
                  DEPENDS inc/test.h inc/test2/test2.h
                  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/..
                  VERBATIM)

add_library(H5Transform
            INTERFACE)

add_definitions(${HDF5_DEFINITIONS})
               
target_link_libraries(H5Transform
                      INTERFACE
                      ${HDF5_LIBRARIES} 
                      "hdf5_cpp")

target_include_directories(H5Transform
                           INTERFACE
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
                           $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_compile_features(H5Transform
                        INTERFACE
                        cxx_std_11)

install(TARGETS H5Transform
        EXPORT ${PROJECT_NAME}_Targets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_ISNTALL_LIBDIR})
        
write_basic_package_version_file("${PROJECT_NAME}ConfigVersion.cmake"
                                 VERSION ${PROJECT_VERSION}
                                 COMPATIBILITY SameMajorVersion)

configure_package_config_file("${PROJECT_SOURCE_DIR}/cmake/${PROJECT_NAME}Config.cmake.in"
                              "${PROJECT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
                              INSTALL_DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/cmake)

install(EXPORT ${PROJECT_NAME}_Targets
        FILE ${PROJECT_NAME}Targets.cmake
        NAMESPACE ${PROJECT_NAME}::
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/cmake)

install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/H5Transform DESTINATION include)

set(CPACK_RESOURCE_FILE_LICENSE "${PROJECT_SOURCE_DIR}/LICENSE")

include(CPack)