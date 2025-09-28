/**
 * @file test_oop_system.c
 * @brief Unit tests for FHIR OOP system
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include "../common/fhir_resource_base.h"
#include "../resources/fhir_patient.h"
#include <string.h>

/* ========================================================================== */
/* Resource Base System Tests                                                */
/* ========================================================================== */

bool test_resource_type_conversion(void) {
    // Test type to string conversion
    ASSERT_STR_EQ("Patient", fhir_resource_type_to_string(FHIR_RESOURCE_TYPE_PATIENT));
    ASSERT_STR_EQ("Practitioner", fhir_resource_type_to_string(FHIR_RESOURCE_TYPE_PRACTITIONER));
    ASSERT_STR_EQ("Encounter", fhir_resource_type_to_string(FHIR_RESOURCE_TYPE_ENCOUNTER));
    
    // Test invalid type
    ASSERT_NULL(fhir_resource_type_to_string(FHIR_RESOURCE_TYPE_UNKNOWN));
    ASSERT_NULL(fhir_resource_type_to_string(FHIR_RESOURCE_TYPE_COUNT));
    
    // Test string to type conversion
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, fhir_resource_type_from_string("Patient"));
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PRACTITIONER, fhir_resource_type_from_string("Practitioner"));
    ASSERT_EQ(FHIR_RESOURCE_TYPE_ENCOUNTER, fhir_resource_type_from_string("Encounter"));
    
    // Test invalid string
    ASSERT_EQ(FHIR_RESOURCE_TYPE_UNKNOWN, fhir_resource_type_from_string("InvalidType"));
    ASSERT_EQ(FHIR_RESOURCE_TYPE_UNKNOWN, fhir_resource_type_from_string(NULL));
    
    return true;
}

bool test_resource_type_validation(void) {
    // Test valid types
    ASSERT_TRUE(fhir_resource_type_is_valid(FHIR_RESOURCE_TYPE_PATIENT));
    ASSERT_TRUE(fhir_resource_type_is_valid(FHIR_RESOURCE_TYPE_PRACTITIONER));
    ASSERT_TRUE(fhir_resource_type_is_valid(FHIR_RESOURCE_TYPE_ENCOUNTER));
    
    // Test invalid types
    ASSERT_FALSE(fhir_resource_type_is_valid(FHIR_RESOURCE_TYPE_UNKNOWN));
    ASSERT_FALSE(fhir_resource_type_is_valid(FHIR_RESOURCE_TYPE_COUNT));
    ASSERT_FALSE(fhir_resource_type_is_valid((FHIRResourceType)-1));
    ASSERT_FALSE(fhir_resource_type_is_valid((FHIRResourceType)999));
    
    return true;
}

/* ========================================================================== */
/* Patient Resource Tests                                                     */
/* ========================================================================== */

bool test_patient_creation_and_destruction(void) {
    // Test successful creation
    FHIRPatient* patient = fhir_patient_create("test-patient-123");
    ASSERT_NOT_NULL(patient);
    ASSERT_STR_EQ("test-patient-123", patient->base.id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient->base.resource_type);
    ASSERT_EQ(1, patient->base.ref_count);
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, patient->gender);
    
    // Test virtual method dispatch
    ASSERT_NOT_NULL(patient->base.vtable);
    ASSERT_STR_EQ("Patient", patient->base.vtable->resource_type_name);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient->base.vtable->resource_type);
    
    // Test destruction
    fhir_patient_destroy(patient);
    
    // Test invalid creation
    FHIRPatient* invalid_patient = fhir_patient_create(NULL);
    ASSERT_NULL(invalid_patient);
    
    invalid_patient = fhir_patient_create("");
    ASSERT_NULL(invalid_patient);
    
    invalid_patient = fhir_patient_create("invalid id with spaces");
    ASSERT_NULL(invalid_patient);
    
    return true;
}

bool test_patient_reference_counting(void) {
    FHIRPatient* patient = fhir_patient_create("test-patient-ref");
    ASSERT_NOT_NULL(patient);
    ASSERT_EQ(1, fhir_resource_get_ref_count((FHIRResourceBase*)patient));
    
    // Test retain
    FHIRResourceBase* retained = fhir_resource_retain((FHIRResourceBase*)patient);
    ASSERT_EQ(patient, retained);
    ASSERT_EQ(2, fhir_resource_get_ref_count((FHIRResourceBase*)patient));
    
    // Test release (should not destroy yet)
    fhir_resource_release((FHIRResourceBase*)patient);
    ASSERT_EQ(1, fhir_resource_get_ref_count((FHIRResourceBase*)patient));
    
    // Test final release (should destroy)
    fhir_resource_release((FHIRResourceBase*)patient);
    // Patient should be destroyed now, can't test further
    
    return true;
}

bool test_patient_polymorphic_methods(void) {
    FHIRPatient* patient = fhir_patient_create("test-patient-poly");
    ASSERT_NOT_NULL(patient);
    
    FHIRResourceBase* base = (FHIRResourceBase*)patient;
    
    // Test polymorphic validation
    ASSERT_TRUE(fhir_resource_validate(base));
    
    // Test polymorphic active check (should be false by default)
    ASSERT_FALSE(fhir_resource_is_active(base));
    
    // Set patient active and test again
    fhir_patient_set_active(patient, true);
    ASSERT_TRUE(fhir_resource_is_active(base));
    
    // Test polymorphic JSON serialization
    cJSON* json = fhir_resource_to_json(base);
    ASSERT_NOT_NULL(json);
    
    // Verify JSON content
    cJSON* resource_type = cJSON_GetObjectItem(json, "resourceType");
    ASSERT_NOT_NULL(resource_type);
    ASSERT_TRUE(cJSON_IsString(resource_type));
    ASSERT_STR_EQ("Patient", resource_type->valuestring);
    
    cJSON* id = cJSON_GetObjectItem(json, "id");
    ASSERT_NOT_NULL(id);
    ASSERT_TRUE(cJSON_IsString(id));
    ASSERT_STR_EQ("test-patient-poly", id->valuestring);
    
    cJSON* active = cJSON_GetObjectItem(json, "active");
    ASSERT_NOT_NULL(active);
    ASSERT_TRUE(cJSON_IsBool(active));
    ASSERT_TRUE(cJSON_IsTrue(active));
    
    cJSON_Delete(json);
    fhir_patient_destroy(patient);
    
    return true;
}

bool test_patient_specific_methods(void) {
    FHIRPatient* patient = fhir_patient_create("test-patient-methods");
    ASSERT_NOT_NULL(patient);
    
    // Test gender methods
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, patient->gender);
    ASSERT_TRUE(fhir_patient_set_gender(patient, FHIR_PATIENT_GENDER_FEMALE));
    ASSERT_EQ(FHIR_PATIENT_GENDER_FEMALE, patient->gender);
    
    // Test birth date methods
    ASSERT_NULL(patient->birth_date);
    ASSERT_TRUE(fhir_patient_set_birth_date(patient, "1990-05-15"));
    ASSERT_NOT_NULL(patient->birth_date);
    ASSERT_STR_EQ("1990-05-15", patient->birth_date->value);
    
    // Test invalid birth date
    ASSERT_FALSE(fhir_patient_set_birth_date(patient, "invalid-date"));
    ASSERT_STR_EQ("1990-05-15", patient->birth_date->value); // Should remain unchanged
    
    // Test deceased status
    ASSERT_FALSE(fhir_patient_is_deceased(patient));
    
    // Test string representation
    char* str = fhir_patient_to_string(patient);
    ASSERT_NOT_NULL(str);
    // Should contain patient info
    ASSERT_TRUE(strstr(str, "Patient") != NULL);
    ASSERT_TRUE(strstr(str, "test-patient-methods") != NULL);
    free(str);
    
    fhir_patient_destroy(patient);
    
    return true;
}

bool test_patient_gender_conversion(void) {
    // Test gender to string conversion
    ASSERT_STR_EQ("unknown", fhir_patient_gender_to_string(FHIR_PATIENT_GENDER_UNKNOWN));
    ASSERT_STR_EQ("male", fhir_patient_gender_to_string(FHIR_PATIENT_GENDER_MALE));
    ASSERT_STR_EQ("female", fhir_patient_gender_to_string(FHIR_PATIENT_GENDER_FEMALE));
    ASSERT_STR_EQ("other", fhir_patient_gender_to_string(FHIR_PATIENT_GENDER_OTHER));
    
    // Test invalid gender
    ASSERT_NULL(fhir_patient_gender_to_string((FHIRPatientGender)-1));
    ASSERT_NULL(fhir_patient_gender_to_string((FHIRPatientGender)999));
    
    // Test string to gender conversion
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, fhir_patient_gender_from_string("unknown"));
    ASSERT_EQ(FHIR_PATIENT_GENDER_MALE, fhir_patient_gender_from_string("male"));
    ASSERT_EQ(FHIR_PATIENT_GENDER_FEMALE, fhir_patient_gender_from_string("female"));
    ASSERT_EQ(FHIR_PATIENT_GENDER_OTHER, fhir_patient_gender_from_string("other"));
    
    // Test invalid string
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, fhir_patient_gender_from_string("invalid"));
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, fhir_patient_gender_from_string(NULL));
    
    return true;
}

bool test_patient_json_serialization(void) {
    FHIRPatient* patient = fhir_patient_create("test-patient-json");
    ASSERT_NOT_NULL(patient);
    
    // Set some fields
    fhir_patient_set_active(patient, true);
    fhir_patient_set_gender(patient, FHIR_PATIENT_GENDER_MALE);
    fhir_patient_set_birth_date(patient, "1985-12-25");
    
    // Test JSON serialization
    cJSON* json = fhir_patient_to_json(patient);
    ASSERT_NOT_NULL(json);
    
    // Convert to string and back
    char* json_string = cJSON_Print(json);
    ASSERT_NOT_NULL(json_string);
    
    // Parse back to patient
    FHIRPatient* parsed_patient = fhir_patient_parse(json_string);
    ASSERT_NOT_NULL(parsed_patient);
    
    // Verify parsed data
    ASSERT_STR_EQ("test-patient-json", parsed_patient->base.id);
    ASSERT_NOT_NULL(parsed_patient->active);
    ASSERT_TRUE(parsed_patient->active->value);
    ASSERT_EQ(FHIR_PATIENT_GENDER_MALE, parsed_patient->gender);
    ASSERT_NOT_NULL(parsed_patient->birth_date);
    ASSERT_STR_EQ("1985-12-25", parsed_patient->birth_date->value);
    
    // Test equality
    ASSERT_TRUE(fhir_patient_equals(patient, parsed_patient));
    
    // Cleanup
    cJSON_Delete(json);
    free(json_string);
    fhir_patient_destroy(patient);
    fhir_patient_destroy(parsed_patient);
    
    return true;
}

/* ========================================================================== */
/* Resource Factory Tests                                                     */
/* ========================================================================== */

bool test_resource_registration_and_factory(void) {
    // Register Patient resource type
    ASSERT_TRUE(fhir_patient_register());
    
    // Test factory creation by name
    FHIRResourceBase* patient_base = fhir_resource_create_by_name("Patient", "factory-test-123");
    ASSERT_NOT_NULL(patient_base);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient_base->resource_type);
    ASSERT_STR_EQ("factory-test-123", patient_base->id);
    
    // Cast to specific type and test
    FHIRPatient* patient = (FHIRPatient*)patient_base;
    ASSERT_EQ(FHIR_PATIENT_GENDER_UNKNOWN, patient->gender);
    
    // Test factory creation by type
    FHIRResourceBase* patient_base2 = fhir_resource_create_by_type(FHIR_RESOURCE_TYPE_PATIENT, "factory-test-456");
    ASSERT_NOT_NULL(patient_base2);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PATIENT, patient_base2->resource_type);
    ASSERT_STR_EQ("factory-test-456", patient_base2->id);
    
    // Test invalid resource type
    FHIRResourceBase* invalid = fhir_resource_create_by_name("InvalidResource", "test");
    ASSERT_NULL(invalid);
    
    invalid = fhir_resource_create_by_type(FHIR_RESOURCE_TYPE_UNKNOWN, "test");
    ASSERT_NULL(invalid);
    
    // Cleanup
    fhir_resource_release(patient_base);
    fhir_resource_release(patient_base2);
    
    return true;
}

/* ========================================================================== */
/* Main Test Runner                                                           */
/* ========================================================================== */

int main(void) {
    TEST_INIT();
    
    // Resource base system tests
    RUN_TEST(test_resource_type_conversion);
    RUN_TEST(test_resource_type_validation);
    
    // Patient resource tests
    RUN_TEST(test_patient_creation_and_destruction);
    RUN_TEST(test_patient_reference_counting);
    RUN_TEST(test_patient_polymorphic_methods);
    RUN_TEST(test_patient_specific_methods);
    RUN_TEST(test_patient_gender_conversion);
    RUN_TEST(test_patient_json_serialization);
    
    // Resource factory tests
    RUN_TEST(test_resource_registration_and_factory);
    
    TEST_FINALIZE();
    return 0;
}