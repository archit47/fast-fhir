/**
 * @file test_practitionerrole.c
 * @brief Unit tests for FHIR PractitionerRole resource with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include "../resources/fhir_practitionerrole.h"
#include "../common/fhir_common.h"
#include <stdio.h>
#include <string.h>
#include <assert.h>

/* ========================================================================== */
/* Test PractitionerRole Creation and Destruction                            */
/* ========================================================================== */

bool test_practitionerrole_create_destroy(void) {
    TEST_START("PractitionerRole Create/Destroy");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create("role-123");
    ASSERT_NOT_NULL(role);
    ASSERT_STR_EQ("role-123", role->base.id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PRACTITIONERROLE, role->base.resource_type);
    ASSERT_NOT_NULL(role->base.vtable);
    ASSERT_EQ(1, role->base.ref_count);
    
    // Test default values
    ASSERT_NOT_NULL(role->active);
    ASSERT_TRUE(role->active->value);
    
    fhir_practitionerrole_destroy(role);
    
    TEST_PASS();
}

bool test_practitionerrole_invalid_id(void) {
    TEST_START("PractitionerRole Invalid ID");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create(NULL);
    ASSERT_NULL(role);
    
    role = fhir_practitionerrole_create("");
    ASSERT_NULL(role);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test PractitionerRole Polymorphism                                        */
/* ========================================================================== */

bool test_practitionerrole_polymorphism(void) {
    TEST_START("PractitionerRole Polymorphism");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create("role-123");
    ASSERT_NOT_NULL(role);
    
    // Test polymorphic casting
    FHIRResourceBase* base = (FHIRResourceBase*)role;
    ASSERT_NOT_NULL(base);
    ASSERT_STR_EQ("role-123", base->id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PRACTITIONERROLE, base->resource_type);
    
    // Test virtual method calls
    ASSERT_TRUE(fhir_resource_validate(base));
    ASSERT_TRUE(fhir_resource_is_active(base));
    
    const char* display_name = fhir_resource_get_display_name(base);
    ASSERT_NOT_NULL(display_name);
    
    cJSON* json = fhir_resource_to_json(base);
    ASSERT_NOT_NULL(json);
    
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("PractitionerRole", resource_type);
    
    cJSON_Delete(json);
    fhir_resource_release(base);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test PractitionerRole JSON Serialization                                  */
/* ========================================================================== */

bool test_practitionerrole_json_serialization(void) {
    TEST_START("PractitionerRole JSON Serialization");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create("role-123");
    ASSERT_NOT_NULL(role);
    
    // Test JSON serialization
    cJSON* json = fhir_practitionerrole_to_json(role);
    ASSERT_NOT_NULL(json);
    
    // Verify JSON content
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("PractitionerRole", resource_type);
    
    const char* id = fhir_json_get_string(json, "id");
    ASSERT_STR_EQ("role-123", id);
    
    const cJSON* active_json = cJSON_GetObjectItem(json, "active");
    ASSERT_NOT_NULL(active_json);
    ASSERT_TRUE(cJSON_IsTrue(active_json));
    
    // Test polymorphic serialization
    cJSON* poly_json = fhir_resource_to_json((FHIRResourceBase*)role);
    ASSERT_NOT_NULL(poly_json);
    
    const char* poly_resource_type = fhir_json_get_string(poly_json, "resourceType");
    ASSERT_STR_EQ("PractitionerRole", poly_resource_type);
    
    cJSON_Delete(json);
    cJSON_Delete(poly_json);
    fhir_practitionerrole_destroy(role);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test PractitionerRole Validation                                          */
/* ========================================================================== */

bool test_practitionerrole_validation(void) {
    TEST_START("PractitionerRole Validation");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create("role-123");
    ASSERT_NOT_NULL(role);
    
    // Without required fields, validation should fail
    ASSERT_FALSE(fhir_practitionerrole_validate(role));
    ASSERT_FALSE(fhir_resource_validate((FHIRResourceBase*)role));
    
    // Add required practitioner reference
    role->practitioner = fhir_reference_create();
    ASSERT_NOT_NULL(role->practitioner);
    role->practitioner->reference = fhir_string_create("Practitioner/prac-123");
    
    // Still missing organization
    ASSERT_FALSE(fhir_practitionerrole_validate(role));
    
    // Add required organization reference
    role->organization = fhir_reference_create();
    ASSERT_NOT_NULL(role->organization);
    role->organization->reference = fhir_string_create("Organization/org-456");
    
    // Now validation should pass
    ASSERT_TRUE(fhir_practitionerrole_validate(role));
    ASSERT_TRUE(fhir_resource_validate((FHIRResourceBase*)role));
    
    // Test with NULL
    ASSERT_FALSE(fhir_practitionerrole_validate(NULL));
    
    fhir_practitionerrole_destroy(role);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test PractitionerRole-Specific Methods                                    */
/* ========================================================================== */

bool test_practitionerrole_specific_methods(void) {
    TEST_START("PractitionerRole-Specific Methods");
    
    FHIRPractitionerRole* role = fhir_practitionerrole_create("role-123");
    ASSERT_NOT_NULL(role);
    
    // Test active status
    ASSERT_TRUE(fhir_practitionerrole_is_active(role));
    
    // Set inactive
    if (role->active) {
        role->active->value = false;
    }
    ASSERT_FALSE(fhir_practitionerrole_is_active(role));
    
    // Test display name
    const char* display_name = fhir_practitionerrole_get_display_name(role);
    ASSERT_NOT_NULL(display_name);
    ASSERT_STR_EQ("PractitionerRole", display_name);
    
    // Test with practitioner reference display
    role->practitioner = fhir_reference_create();
    ASSERT_NOT_NULL(role->practitioner);
    role->practitioner->display = fhir_string_create("Dr. John Smith");
    
    display_name = fhir_practitionerrole_get_display_name(role);
    ASSERT_NOT_NULL(display_name);
    ASSERT_STR_EQ("Dr. John Smith", display_name);
    
    fhir_practitionerrole_destroy(role);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test PractitionerRole Factory Registration                                */
/* ========================================================================== */

bool test_practitionerrole_factory_registration(void) {
    TEST_START("PractitionerRole Factory Registration");
    
    // Register practitionerrole resource type
    bool result = fhir_practitionerrole_register();
    ASSERT_TRUE(result);
    
    // Test factory creation
    FHIRResourceBase* role = fhir_resource_create_by_name("PractitionerRole", "factory-test");
    ASSERT_NOT_NULL(role);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_PRACTITIONERROLE, role->resource_type);
    ASSERT_STR_EQ("factory-test", role->id);
    
    // Test polymorphic behavior
    ASSERT_TRUE(fhir_resource_is_active(role));
    
    fhir_resource_release(role);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Main Test Runner                                                          */
/* ========================================================================== */

int main(void) {
    TEST_INIT();
    
    printf("Running PractitionerRole Resource Tests...\n\n");
    
    // Basic functionality tests
    RUN_TEST(test_practitionerrole_create_destroy);
    RUN_TEST(test_practitionerrole_invalid_id);
    
    // OOP functionality tests
    RUN_TEST(test_practitionerrole_polymorphism);
    
    // Serialization tests
    RUN_TEST(test_practitionerrole_json_serialization);
    
    // Validation tests
    RUN_TEST(test_practitionerrole_validation);
    
    // PractitionerRole-specific tests
    RUN_TEST(test_practitionerrole_specific_methods);
    
    // Factory tests
    RUN_TEST(test_practitionerrole_factory_registration);
    
    TEST_FINALIZE();
    
    return 0;
}