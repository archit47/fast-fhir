/**
 * @file test_patient.c
 * @brief Unit tests for FHIR Patient resource with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include "../resources/fhir_patient.h"
#include "../common/fhir_common.h"
#include <stdio.h>
#include <string.h>
#include <assert.h>

/* ========================================================================== */
/* Test Patient Creation and Destruction                                     */
/* ========================================================================== */

bool test_patient_create_destroy(void) {
    TEST_START("Patient Create/Destroy");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    ASSERT_STR_EQ("patient-123", patient->base.id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient->base.resource_type);
    ASSERT_NOT_NULL(patient->base.vtable);
    ASSERT_EQ(1, patient->base.ref_count);
    
    // Test default values
    ASSERT_NOT_NULL(patient->active);
    ASSERT_TRUE(patient->active->value);
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, patient->gender);
    
    fhir_patient_destroy(patient);
    
    TEST_PASS();
}

bool test_patient_invalid_id(void) {
    TEST_START("Patient Invalid ID");
    
    FHIRPatient* patient = fhir_patient_create(NULL);
    ASSERT_NULL(patient);
    
    patient = fhir_patient_create("");
    ASSERT_NULL(patient);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient Polymorphism                                                 */
/* ========================================================================== */

bool test_patient_polymorphism(void) {
    TEST_START("Patient Polymorphism");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    
    // Test polymorphic casting
    FHIRResourceBase* base = (FHIRResourceBase*)patient;
    ASSERT_NOT_NULL(base);
    ASSERT_STR_EQ("patient-123", base->id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, base->resource_type);
    
    // Test virtual method calls
    ASSERT_TRUE(fhir_resource_validate(base));
    ASSERT_TRUE(fhir_resource_is_active(base));
    
    const char* display_name = fhir_resource_get_display_name(base);
    ASSERT_NOT_NULL(display_name);
    
    cJSON* json = fhir_resource_to_json(base);
    ASSERT_NOT_NULL(json);
    
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("Patient", resource_type);
    
    cJSON_Delete(json);
    fhir_resource_release(base);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient Reference Counting                                           */
/* ========================================================================== */

bool test_patient_reference_counting(void) {
    TEST_START("Patient Reference Counting");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    ASSERT_EQ(1, patient->base.ref_count);
    
    // Retain reference
    FHIRResourceBase* retained = fhir_resource_retain((FHIRResourceBase*)patient);
    ASSERT_NOT_NULL(retained);
    ASSERT_EQ(2, patient->base.ref_count);
    ASSERT_EQ(patient, (FHIRPatient*)retained);
    
    // Release one reference
    fhir_resource_release((FHIRResourceBase*)patient);
    ASSERT_EQ(1, ((FHIRResourceBase*)retained)->ref_count);
    
    // Release final reference
    fhir_resource_release(retained);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient Cloning                                                      */
/* ========================================================================== */

bool test_patient_cloning(void) {
    TEST_START("Patient Cloning");
    
    FHIRPatient* original = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(original);
    
    // Set some properties
    fhir_patient_set_gender(original, FHIR_PATIENT_GENDER_FEMALE);
    fhir_patient_set_birth_date(original, "1990-05-15");
    
    // Clone the patient
    FHIRPatient* clone = fhir_patient_clone(original);
    ASSERT_NOT_NULL(clone);
    ASSERT_STR_EQ(original->base.id, clone->base.id);
    ASSERT_EQ(original->gender, clone->gender);
    
    // Verify they are separate objects
    ASSERT_NE(original, clone);
    ASSERT_EQ(1, original->base.ref_count);
    ASSERT_EQ(1, clone->base.ref_count);
    
    // Test polymorphic cloning
    FHIRResourceBase* base_clone = fhir_resource_clone((FHIRResourceBase*)original);
    ASSERT_NOT_NULL(base_clone);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, base_clone->resource_type);
    
    fhir_patient_destroy(original);
    fhir_patient_destroy(clone);
    fhir_resource_release(base_clone);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient JSON Serialization                                           */
/* ========================================================================== */

bool test_patient_json_serialization(void) {
    TEST_START("Patient JSON Serialization");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    
    // Set patient properties
    fhir_patient_set_active(patient, true);
    fhir_patient_set_gender(patient, FHIR_PATIENT_GENDER_FEMALE);
    fhir_patient_set_birth_date(patient, "1990-05-15");
    
    // Test JSON serialization
    cJSON* json = fhir_patient_to_json(patient);
    ASSERT_NOT_NULL(json);
    
    // Verify JSON content
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("Patient", resource_type);
    
    const char* id = fhir_json_get_string(json, "id");
    ASSERT_STR_EQ("patient-123", id);
    
    const cJSON* active_json = cJSON_GetObjectItem(json, "active");
    ASSERT_NOT_NULL(active_json);
    ASSERT_TRUE(cJSON_IsTrue(active_json));
    
    const char* gender = fhir_json_get_string(json, "gender");
    ASSERT_STR_EQ("female", gender);
    
    const char* birth_date = fhir_json_get_string(json, "birthDate");
    ASSERT_STR_EQ("1990-05-15", birth_date);
    
    // Test polymorphic serialization
    cJSON* poly_json = fhir_resource_to_json((FHIRResourceBase*)patient);
    ASSERT_NOT_NULL(poly_json);
    
    const char* poly_resource_type = fhir_json_get_string(poly_json, "resourceType");
    ASSERT_STR_EQ("Patient", poly_resource_type);
    
    cJSON_Delete(json);
    cJSON_Delete(poly_json);
    fhir_patient_destroy(patient);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient JSON Deserialization                                         */
/* ========================================================================== */

bool test_patient_json_deserialization(void) {
    TEST_START("Patient JSON Deserialization");
    
    const char* json_string = "{"
        "\"resourceType\": \"Patient\","
        "\"id\": \"patient-456\","
        "\"active\": true,"
        "\"gender\": \"male\","
        "\"birthDate\": \"1985-12-25\""
    "}";
    
    // Test parsing from string
    FHIRPatient* patient = fhir_patient_parse(json_string);
    ASSERT_NOT_NULL(patient);
    ASSERT_STR_EQ("patient-456", patient->base.id);
    ASSERT_TRUE(patient->active->value);
    ASSERT_EQ(FHIR_PATIENT_GENDER_MALE, patient->gender);
    
    if (patient->birth_date && patient->birth_date->value) {
        ASSERT_STR_EQ("1985-12-25", patient->birth_date->value);
    }
    
    // Test JSON object parsing
    cJSON* json = cJSON_Parse(json_string);
    ASSERT_NOT_NULL(json);
    
    FHIRPatient* patient2 = fhir_patient_create("temp");
    ASSERT_NOT_NULL(patient2);
    
    bool result = fhir_patient_from_json(patient2, json);
    ASSERT_TRUE(result);
    
    cJSON_Delete(json);
    fhir_patient_destroy(patient);
    fhir_patient_destroy(patient2);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient Validation                                                   */
/* ========================================================================== */

bool test_patient_validation(void) {
    TEST_START("Patient Validation");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    
    // Valid patient should pass validation
    ASSERT_TRUE(fhir_patient_validate(patient));
    ASSERT_TRUE(fhir_resource_validate((FHIRResourceBase*)patient));
    
    // Test with NULL
    ASSERT_FALSE(fhir_patient_validate(NULL));
    
    fhir_patient_destroy(patient);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient-Specific Methods                                             */
/* ========================================================================== */

bool test_patient_specific_methods(void) {
    TEST_START("Patient-Specific Methods");
    
    FHIRPatient* patient = fhir_patient_create("patient-123");
    ASSERT_NOT_NULL(patient);
    
    // Test active status
    ASSERT_TRUE(fhir_patient_is_active(patient));
    fhir_patient_set_active(patient, false);
    ASSERT_FALSE(fhir_patient_is_active(patient));
    
    // Test gender
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, patient->gender);
    fhir_patient_set_gender(patient, FHIR_PATIENT_GENDER_FEMALE);
    ASSERT_EQ(FHIR_PATIENT_GENDER_FEMALE, patient->gender);
    
    // Test birth date
    bool result = fhir_patient_set_birth_date(patient, "1990-05-15");
    ASSERT_TRUE(result);
    ASSERT_NOT_NULL(patient->birth_date);
    if (patient->birth_date && patient->birth_date->value) {
        ASSERT_STR_EQ("1990-05-15", patient->birth_date->value);
    }
    
    // Test deceased status
    ASSERT_FALSE(fhir_patient_is_deceased(patient));
    fhir_patient_set_deceased_boolean(patient, true);
    ASSERT_TRUE(fhir_patient_is_deceased(patient));
    
    // Test display name
    const char* display_name = fhir_patient_get_display_name(patient);
    ASSERT_NOT_NULL(display_name);
    
    fhir_patient_destroy(patient);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Patient Factory Registration                                         */
/* ========================================================================== */

bool test_patient_factory_registration(void) {
    TEST_START("Patient Factory Registration");
    
    // Register patient resource type
    bool result = fhir_patient_register();
    ASSERT_TRUE(result);
    
    // Test factory creation
    FHIRResourceBase* patient = fhir_resource_create_by_name("Patient", "factory-test");
    ASSERT_NOT_NULL(patient);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient->resource_type);
    ASSERT_STR_EQ("factory-test", patient->id);
    
    // Test polymorphic behavior
    ASSERT_TRUE(fhir_resource_validate(patient));
    ASSERT_TRUE(fhir_resource_is_active(patient));
    
    fhir_resource_release(patient);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Main Test Runner                                                          */
/* ========================================================================== */

int main(void) {
    TEST_INIT();
    
    printf("Running Patient Resource Tests...\n\n");
    
    // Basic functionality tests
    RUN_TEST(test_patient_create_destroy);
    RUN_TEST(test_patient_invalid_id);
    
    // OOP functionality tests
    RUN_TEST(test_patient_polymorphism);
    RUN_TEST(test_patient_reference_counting);
    RUN_TEST(test_patient_cloning);
    
    // Serialization tests
    RUN_TEST(test_patient_json_serialization);
    RUN_TEST(test_patient_json_deserialization);
    
    // Validation tests
    RUN_TEST(test_patient_validation);
    
    // Patient-specific tests
    RUN_TEST(test_patient_specific_methods);
    
    // Factory tests
    RUN_TEST(test_patient_factory_registration);
    
    TEST_FINALIZE();
    
    return 0;
}