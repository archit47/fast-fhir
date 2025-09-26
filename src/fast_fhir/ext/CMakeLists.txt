# CMakeLists.txt for FHIR C Extensions
# Modern CMake configuration following best practices

cmake_minimum_required(VERSION 3.12)
project(fhir_c_extensions 
    VERSION 1.0.0
    DESCRIPTION "FHIR R5 C Extensions"
    LANGUAGES C)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -DDEBUG -fsanitize=address")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")

# Warning flags
add_compile_options(
    -Wall
    -Wextra
    -Wpedantic
    -Wformat=2
    -Wno-unused-parameter
    -Wshadow
    -Wwrite-strings
    -Wstrict-prototypes
    -Wold-style-definition
    -Wredundant-decls
    -Wnested-externs
    -Wmissing-include-dirs
)

# Find required packages
find_package(PkgConfig REQUIRED)
pkg_check_modules(CJSON REQUIRED libcjson)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/common
    ${CMAKE_CURRENT_SOURCE_DIR}/resources
    ${CJSON_INCLUDE_DIRS}
    ${Python3_INCLUDE_DIRS}
)

# Link directories
link_directories(${CJSON_LIBRARY_DIRS})

# Compiler definitions
add_definitions(${CJSON_CFLAGS_OTHER})

# ============================================================================
# Common Library
# ============================================================================

set(COMMON_SOURCES
    common/fhir_common.c
    common/fhir_resource_base.c
)

set(COMMON_HEADERS
    common/fhir_common.h
    common/fhir_resource_base.h
    fhir_datatypes.h
)

add_library(fhir_common STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})
target_link_libraries(fhir_common ${CJSON_LIBRARIES})

# ============================================================================
# Resource Libraries
# ============================================================================

# Foundation Resources
add_library(fhir_patient SHARED
    resources/fhir_patient.c
    resources/fhir_patient.h
)
target_link_libraries(fhir_patient fhir_common ${CJSON_LIBRARIES})

add_library(fhir_practitioner SHARED
    resources/fhir_practitioner.c
    resources/fhir_practitioner.h
)
target_link_libraries(fhir_practitioner fhir_common ${CJSON_LIBRARIES})

add_library(fhir_practitionerrole SHARED
    resources/fhir_practitionerrole.c
    resources/fhir_practitionerrole.h
)
target_link_libraries(fhir_practitionerrole fhir_common ${CJSON_LIBRARIES})

add_library(fhir_organization SHARED
    resources/fhir_organization.c
    resources/fhir_organization.h
)
target_link_libraries(fhir_organization fhir_common ${CJSON_LIBRARIES})

add_library(fhir_organization_affiliation SHARED
    resources/fhir_organization_affiliation.c
    resources/fhir_organization_affiliation.h
)
target_link_libraries(fhir_organization_affiliation fhir_common ${CJSON_LIBRARIES})

add_library(fhir_location SHARED
    resources/fhir_location.c
    resources/fhir_location.h
)
target_link_libraries(fhir_location fhir_common ${CJSON_LIBRARIES})

add_library(fhir_healthcare_service SHARED
    resources/fhir_healthcare_service.c
    resources/fhir_healthcare_service.h
)
target_link_libraries(fhir_healthcare_service fhir_common ${CJSON_LIBRARIES})

add_library(fhir_endpoint SHARED
    resources/fhir_endpoint.c
    resources/fhir_endpoint.h
)
target_link_libraries(fhir_endpoint fhir_common ${CJSON_LIBRARIES})

# Clinical Resources
add_library(fhir_encounter SHARED
    resources/fhir_encounter.c
    resources/fhir_encounter.h
)
target_link_libraries(fhir_encounter fhir_common ${CJSON_LIBRARIES})

add_library(fhir_observation SHARED
    resources/fhir_observation.c
    resources/fhir_observation.h
)
target_link_libraries(fhir_observation fhir_common ${CJSON_LIBRARIES})

# Clinical Resources (Care Provision)
add_library(fhir_careplan SHARED
    resources/fhir_careplan.c
    resources/fhir_careplan.h
)
target_link_libraries(fhir_careplan fhir_common ${CJSON_LIBRARIES})

add_library(fhir_careteam SHARED
    resources/fhir_careteam.c
    resources/fhir_careteam.h
)
target_link_libraries(fhir_careteam fhir_common ${CJSON_LIBRARIES})

add_library(fhir_goal SHARED
    resources/fhir_goal.c
    resources/fhir_goal.h
)
target_link_libraries(fhir_goal fhir_common ${CJSON_LIBRARIES})

add_library(fhir_servicerequest SHARED
    resources/fhir_servicerequest.c
    resources/fhir_servicerequest.h
)
target_link_libraries(fhir_servicerequest fhir_common ${CJSON_LIBRARIES})

add_library(fhir_nutritionorder SHARED
    resources/fhir_nutritionorder.c
    resources/fhir_nutritionorder.h
)
target_link_libraries(fhir_nutritionorder fhir_common ${CJSON_LIBRARIES})

add_library(fhir_riskassessment SHARED
    resources/fhir_riskassessment.c
    resources/fhir_riskassessment.h
)
target_link_libraries(fhir_riskassessment fhir_common ${CJSON_LIBRARIES})

add_library(fhir_visionprescription SHARED
    resources/fhir_visionprescription.c
    resources/fhir_visionprescription.h
)
target_link_libraries(fhir_visionprescription fhir_common ${CJSON_LIBRARIES})

add_library(fhir_encounter_history SHARED
    resources/fhir_encounter_history.c
    resources/fhir_encounter_history.h
)
target_link_libraries(fhir_encounter_history fhir_common ${CJSON_LIBRARIES})

add_library(fhir_episode_of_care SHARED
    resources/fhir_episode_of_care.c
    resources/fhir_episode_of_care.h
)
target_link_libraries(fhir_episode_of_care fhir_common ${CJSON_LIBRARIES})

add_library(fhir_observation SHARED
    resources/fhir_observation.c
    resources/fhir_observation.h
)
target_link_libraries(fhir_observation fhir_common ${CJSON_LIBRARIES})

add_library(fhir_condition SHARED
    resources/fhir_condition.c
    resources/fhir_condition.h
)
target_link_libraries(fhir_condition fhir_common ${CJSON_LIBRARIES})

add_library(fhir_procedure SHARED
    resources/fhir_procedure.c
    resources/fhir_procedure.h
)
target_link_libraries(fhir_procedure fhir_common ${CJSON_LIBRARIES})

# Workflow Resources
add_library(fhir_appointment SHARED
    resources/fhir_appointment.c
    resources/fhir_appointment.h
)
target_link_libraries(fhir_appointment fhir_common ${CJSON_LIBRARIES})

add_library(fhir_appointment_response SHARED
    resources/fhir_appointment_response.c
    resources/fhir_appointment_response.h
)
target_link_libraries(fhir_appointment_response fhir_common ${CJSON_LIBRARIES})

add_library(fhir_schedule SHARED
    resources/fhir_schedule.c
    resources/fhir_schedule.h
)
target_link_libraries(fhir_schedule fhir_common ${CJSON_LIBRARIES})

add_library(fhir_slot SHARED
    resources/fhir_slot.c
    resources/fhir_slot.h
)
target_link_libraries(fhir_slot fhir_common ${CJSON_LIBRARIES})

add_library(fhir_task SHARED
    resources/fhir_task.c
    resources/fhir_task.h
)
target_link_libraries(fhir_task fhir_common ${CJSON_LIBRARIES})

add_library(fhir_transport SHARED
    resources/fhir_transport.c
    resources/fhir_transport.h
)
target_link_libraries(fhir_transport fhir_common ${CJSON_LIBRARIES})

# Specialized Resources
add_library(fhir_device SHARED
    resources/fhir_device.c
    resources/fhir_device.h
)
target_link_libraries(fhir_device fhir_common ${CJSON_LIBRARIES})

add_library(fhir_device_metric SHARED
    resources/fhir_device_metric.c
    resources/fhir_device_metric.h
)
target_link_libraries(fhir_device_metric fhir_common ${CJSON_LIBRARIES})

add_library(fhir_biologically_derived_product SHARED
    resources/fhir_biologically_derived_product.c
    resources/fhir_biologically_derived_product.h
)
target_link_libraries(fhir_biologically_derived_product fhir_common ${CJSON_LIBRARIES})

add_library(fhir_nutrition_product SHARED
    resources/fhir_nutrition_product.c
    resources/fhir_nutrition_product.h
)
target_link_libraries(fhir_nutrition_product fhir_common ${CJSON_LIBRARIES})

add_library(fhir_verification_result SHARED
    resources/fhir_verification_result.c
    resources/fhir_verification_result.h
)
target_link_libraries(fhir_verification_result fhir_common ${CJSON_LIBRARIES})

# ============================================================================
# Python Extension
# ============================================================================

add_library(fhir_new_resources_c MODULE
    fhir_new_resources.c
    fhir_new_resources_python.c
)

target_link_libraries(fhir_new_resources_c
    fhir_common
    fhir_patient
    fhir_practitioner
    fhir_practitionerrole
    fhir_organization
    fhir_location
    fhir_encounter
    fhir_observation
    fhir_careplan
    fhir_careteam
    fhir_goal
    fhir_servicerequest
    fhir_nutritionorder
    fhir_riskassessment
    fhir_visionprescription
    fhir_organization_affiliation
    fhir_biologically_derived_product
    fhir_device_metric
    fhir_nutrition_product
    fhir_transport
    fhir_verification_result
    fhir_encounter_history
    fhir_episode_of_care
    ${CJSON_LIBRARIES}
    ${Python3_LIBRARIES}
)

# Set Python extension properties
set_target_properties(fhir_new_resources_c PROPERTIES
    PREFIX ""
    SUFFIX "${Python3_SOABI}${CMAKE_SHARED_LIBRARY_SUFFIX}"
)

# ============================================================================
# Installation
# ============================================================================

# Install libraries
install(TARGETS 
    fhir_common
    fhir_patient
    fhir_practitioner
    fhir_practitionerrole
    fhir_organization
    fhir_location
    fhir_encounter
    fhir_observation
    fhir_careplan
    fhir_careteam
    fhir_goal
    fhir_servicerequest
    fhir_nutritionorder
    fhir_riskassessment
    fhir_visionprescription
    fhir_organization_affiliation
    fhir_biologically_derived_product
    fhir_device_metric
    fhir_nutrition_product
    fhir_transport
    fhir_verification_result
    fhir_encounter_history
    fhir_episode_of_care
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install headers
install(FILES ${COMMON_HEADERS} DESTINATION include/fhir/common)
install(DIRECTORY resources/ DESTINATION include/fhir/resources
    FILES_MATCHING PATTERN "*.h")

# Install Python extension
install(TARGETS fhir_new_resources_c
    LIBRARY DESTINATION ${Python3_SITEARCH})

# ============================================================================
# Testing
# ============================================================================

enable_testing()

# Unit tests for common utilities
add_executable(test_common tests/test_common.c)
target_link_libraries(test_common fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_common COMMAND test_common)

# Unit tests for OOP system
add_executable(test_oop_system tests/test_oop_system.c)
target_link_libraries(test_oop_system 
    fhir_common
    fhir_patient
    fhir_practitioner
    fhir_practitionerrole
    fhir_organization
    fhir_location
    fhir_encounter
    fhir_observation
    ${CJSON_LIBRARIES})
add_test(NAME test_oop_system COMMAND test_oop_system)

# Unit tests for Patient
add_executable(test_patient tests/test_patient.c)
target_link_libraries(test_patient fhir_patient fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_patient COMMAND test_patient)

# Unit tests for Practitioner
add_executable(test_practitioner tests/test_practitioner.c)
target_link_libraries(test_practitioner fhir_practitioner fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_practitioner COMMAND test_practitioner)

# Unit tests for PractitionerRole
add_executable(test_practitionerrole tests/test_practitionerrole.c)
target_link_libraries(test_practitionerrole fhir_practitionerrole fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_practitionerrole COMMAND test_practitionerrole)

# Unit tests for Organization
add_executable(test_organization tests/test_organization.c)
target_link_libraries(test_organization fhir_organization fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_organization COMMAND test_organization)

# Unit tests for Location
add_executable(test_location tests/test_location.c)
target_link_libraries(test_location fhir_location fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_location COMMAND test_location)

# Unit tests for Encounter
add_executable(test_encounter tests/test_encounter.c)
target_link_libraries(test_encounter fhir_encounter fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_encounter COMMAND test_encounter)

# Unit tests for Observation
add_executable(test_observation tests/test_observation.c)
target_link_libraries(test_observation fhir_observation fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_observation COMMAND test_observation)

# Unit tests for Care Provision resources
add_executable(test_care_provision tests/test_care_provision.c)
target_link_libraries(test_care_provision 
    fhir_careplan
    fhir_careteam
    fhir_goal
    fhir_servicerequest
    fhir_nutritionorder
    fhir_riskassessment
    fhir_visionprescription
    fhir_common 
    ${CJSON_LIBRARIES})
add_test(NAME test_care_provision COMMAND test_care_provision)

# Unit tests for OrganizationAffiliation
add_executable(test_organization_affiliation tests/test_organization_affiliation.c)
target_link_libraries(test_organization_affiliation 
    fhir_organization_affiliation fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_organization_affiliation COMMAND test_organization_affiliation)

# Unit tests for DeviceMetric
add_executable(test_device_metric tests/test_device_metric.c)
target_link_libraries(test_device_metric 
    fhir_device_metric fhir_common ${CJSON_LIBRARIES})
add_test(NAME test_device_metric COMMAND test_device_metric)

# Memory leak testing with Valgrind (if available)
find_program(VALGRIND_PROGRAM valgrind)
if(VALGRIND_PROGRAM)
    add_test(NAME test_common_valgrind 
        COMMAND ${VALGRIND_PROGRAM} --leak-check=full --error-exitcode=1 
        $<TARGET_FILE:test_common>)
endif()

# ============================================================================
# Documentation
# ============================================================================

find_package(Doxygen)
if(DOXYGEN_FOUND)
    set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in)
    set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
    
    configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
    
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM)
endif()

# ============================================================================
# Code Analysis
# ============================================================================

# Clang-tidy
find_program(CLANG_TIDY_PROGRAM clang-tidy)
if(CLANG_TIDY_PROGRAM)
    set_target_properties(fhir_common PROPERTIES
        C_CLANG_TIDY "${CLANG_TIDY_PROGRAM};-checks=-*,readability-*,performance-*,bugprone-*")
endif()

# Cppcheck
find_program(CPPCHECK_PROGRAM cppcheck)
if(CPPCHECK_PROGRAM)
    add_custom_target(cppcheck
        COMMAND ${CPPCHECK_PROGRAM} --enable=all --std=c99 --project=${CMAKE_BINARY_DIR}/compile_commands.json
        COMMENT "Running cppcheck static analysis"
        VERBATIM)
endif()

# ============================================================================
# Packaging
# ============================================================================

set(CPACK_PACKAGE_NAME "fhir-c-extensions")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY ${PROJECT_DESCRIPTION})
set(CPACK_PACKAGE_VENDOR "FHIR Implementation Team")
set(CPACK_PACKAGE_CONTACT "team@fhir-implementation.org")

set(CPACK_GENERATOR "TGZ;DEB;RPM")
set(CPACK_SOURCE_GENERATOR "TGZ")

# Debian package configuration
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libcjson1, python3-dev")
set(CPACK_DEBIAN_PACKAGE_SECTION "libs")
set(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")

# RPM package configuration
set(CPACK_RPM_PACKAGE_REQUIRES "cjson, python3-devel")
set(CPACK_RPM_PACKAGE_GROUP "Development/Libraries")

include(CPack)

# ============================================================================
# Development Targets
# ============================================================================

# Format code with clang-format
find_program(CLANG_FORMAT_PROGRAM clang-format)
if(CLANG_FORMAT_PROGRAM)
    file(GLOB_RECURSE ALL_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/*.c
        ${CMAKE_CURRENT_SOURCE_DIR}/*.h
    )
    
    add_custom_target(format
        COMMAND ${CLANG_FORMAT_PROGRAM} -i ${ALL_SOURCE_FILES}
        COMMENT "Formatting source code"
        VERBATIM)
endif()

# Generate compile_commands.json for IDE support
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Print configuration summary
message(STATUS "")
message(STATUS "FHIR C Extensions Configuration Summary:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "  C Standard: C${CMAKE_C_STANDARD}")
message(STATUS "  Install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  Python version: ${Python3_VERSION}")
message(STATUS "  Python site-arch: ${Python3_SITEARCH}")
message(STATUS "  cJSON found: ${CJSON_FOUND}")
message(STATUS "  Doxygen found: ${DOXYGEN_FOUND}")
message(STATUS "  Valgrind found: ${VALGRIND_PROGRAM}")
message(STATUS "  Clang-tidy found: ${CLANG_TIDY_PROGRAM}")
message(STATUS "  Cppcheck found: ${CPPCHECK_PROGRAM}")
message(STATUS "")