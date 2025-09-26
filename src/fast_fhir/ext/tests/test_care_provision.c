/**
 * @file test_care_provision.c
 * @brief Unit tests for FHIR Care Provision resources with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "test_framework.h"
#include "../resources/fhir_careplan.h"
#include "../resources/fhir_careteam.h"
#include "../resources/fhir_goal.h"
#include "../resources/fhir_servicerequest.h"
#include "../resources/fhir_nutritionorder.h"
#include "../resources/fhir_riskassessment.h"
#include "../resources/fhir_visionprescription.h"
#include "../common/fhir_common.h"
#include <stdio.h>
#include <string.h>
#include <assert.h>

/* ========================================================================== */
/* Test CarePlan Resource                                                     */
/* ========================================================================== */

bool test_careplan_creation_and_polymorphism(void) {
    TEST_START("CarePlan Creation and Polymorphism");
    
    FHIRCarePlan* careplan = fhir_careplan_create("careplan-123");
    ASSERT_NOT_NULL(careplan);
    ASSERT_STR_EQ("careplan-123", careplan->base.id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_CAREPLAN, careplan->base.resource_type);
    
    // Test default values
    ASSERT_EQ(FHIR_CAREPLAN_STATUS_DRAFT, careplan->status);
    ASSERT_EQ(FHIR_CAREPLAN_INTENT_PLAN, careplan->intent);
    
    // Test polymorphic behavior
    FHIRResourceBase* base = (FHIRResourceBase*)careplan;
    ASSERT_TRUE(fhir_resource_validate(base));
    
    cJSON* json = fhir_resource_to_json(base);
    ASSERT_NOT_NULL(json);
    
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("CarePlan", resource_type);
    
    // Test status and intent methods
    fhir_careplan_set_status(careplan, FHIR_CAREPLAN_STATUS_ACTIVE);
    ASSERT_EQ(FHIR_CAREPLAN_STATUS_ACTIVE, careplan->status);
    ASSERT_TRUE(fhir_careplan_is_active(careplan));
    
    fhir_careplan_set_intent(careplan, FHIR_CAREPLAN_INTENT_ORDER);
    ASSERT_EQ(FHIR_CAREPLAN_INTENT_ORDER, careplan->intent);
    
    cJSON_Delete(json);
    fhir_careplan_destroy(careplan);
    
    TEST_PASS();
}

bool test_careplan_status_conversion(void) {
    TEST_START("CarePlan Status Conversion");
    
    // Test status to string conversion
    ASSERT_STR_EQ("draft", fhir_careplan_status_to_string(FHIR_CAREPLAN_STATUS_DRAFT));
    ASSERT_STR_EQ("active", fhir_careplan_status_to_string(FHIR_CAREPLAN_STATUS_ACTIVE));
    ASSERT_STR_EQ("completed", fhir_careplan_status_to_string(FHIR_CAREPLAN_STATUS_COMPLETED));
    
    // Test string to status conversion
    ASSERT_EQ(FHIR_CAREPLAN_STATUS_DRAFT, fhir_careplan_status_from_string("draft"));
    ASSERT_EQ(FHIR_CAREPLAN_STATUS_ACTIVE, fhir_careplan_status_from_string("active"));
    ASSERT_EQ(FHIR_CAREPLAN_STATUS_COMPLETED, fhir_careplan_status_from_string("completed"));
    
    // Test intent conversion
    ASSERT_STR_EQ("proposal", fhir_careplan_intent_to_string(FHIR_CAREPLAN_INTENT_PROPOSAL));
    ASSERT_STR_EQ("plan", fhir_careplan_intent_to_string(FHIR_CAREPLAN_INTENT_PLAN));
    ASSERT_STR_EQ("order", fhir_careplan_intent_to_string(FHIR_CAREPLAN_INTENT_ORDER));
    
    ASSERT_EQ(FHIR_CAREPLAN_INTENT_PROPOSAL, fhir_careplan_intent_from_string("proposal"));
    ASSERT_EQ(FHIR_CAREPLAN_INTENT_PLAN, fhir_careplan_intent_from_string("plan"));
    ASSERT_EQ(FHIR_CAREPLAN_INTENT_ORDER, fhir_careplan_intent_from_string("order"));
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test RiskAssessment Resource                                              */
/* ========================================================================== */

bool test_riskassessment_creation_and_functionality(void) {
    TEST_START("RiskAssessment Creation and Functionality");
    
    FHIRRiskAssessment* assessment = fhir_riskassessment_create("risk-123");
    ASSERT_NOT_NULL(assessment);
    ASSERT_STR_EQ("risk-123", assessment->base.id);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_RISKASSESSMENT, assessment->base.resource_type);
    
    // Test default values
    ASSERT_EQ(FHIR_RISKASSESSMENT_STATUS_REGISTERED, assessment->status);
    
    // Test polymorphic behavior
    FHIRResourceBase* base = (FHIRResourceBase*)assessment;
    
    cJSON* json = fhir_resource_to_json(base);
    ASSERT_NOT_NULL(json);
    
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    ASSERT_STR_EQ("RiskAssessment", resource_type);
    
    // Test status methods
    fhir_riskassessment_set_status(assessment, FHIR_RISKASSESSMENT_STATUS_FINAL);
    ASSERT_EQ(FHIR_RISKASSESSMENT_STATUS_FINAL, assessment->status);
    ASSERT_TRUE(fhir_riskassessment_is_active(assessment));
    
    // Test high risk detection
    ASSERT_FALSE(fhir_riskassessment_is_high_risk(assessment, 0.5));
    
    cJSON_Delete(json);
    fhir_riskassessment_destroy(assessment);
    
    TEST_PASS();
}

bool test_riskassessment_status_conversion(void) {
    TEST_START("RiskAssessment Status Conversion");
    
    // Test status to string conversion
    ASSERT_STR_EQ("registered", fhir_riskassessment_status_to_string(FHIR_RISKASSESSMENT_STATUS_REGISTERED));
    ASSERT_STR_EQ("preliminary", fhir_riskassessment_status_to_string(FHIR_RISKASSESSMENT_STATUS_PRELIMINARY));
    ASSERT_STR_EQ("final", fhir_riskassessment_status_to_string(FHIR_RISKASSESSMENT_STATUS_FINAL));
    
    // Test string to status conversion
    ASSERT_EQ(FHIR_RISKASSESSMENT_STATUS_REGISTERED, fhir_riskassessment_status_from_string("registered"));
    ASSERT_EQ(FHIR_RISKASSESSMENT_STATUS_PRELIMINARY, fhir_riskassessment_status_from_string("preliminary"));
    ASSERT_EQ(FHIR_RISKASSESSMENT_STATUS_FINAL, fhir_riskassessment_status_from_string("final"));
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Care Provision Resource Factory                                      */
/* ========================================================================== */

bool test_care_provision_factory_registration(void) {
    TEST_START("Care Provision Factory Registration");
    
    // Register all Care Provision resource types
    ASSERT_TRUE(fhir_careplan_register());
    ASSERT_TRUE(fhir_careteam_register());
    ASSERT_TRUE(fhir_goal_register());
    ASSERT_TRUE(fhir_servicerequest_register());
    ASSERT_TRUE(fhir_nutritionorder_register());
    ASSERT_TRUE(fhir_riskassessment_register());
    ASSERT_TRUE(fhir_visionprescription_register());
    
    // Test factory creation by name
    FHIRResourceBase* careplan = fhir_resource_create_by_name("CarePlan", "plan-123");
    ASSERT_NOT_NULL(careplan);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_CAREPLAN, careplan->resource_type);
    
    FHIRResourceBase* careteam = fhir_resource_create_by_name("CareTeam", "team-456");
    ASSERT_NOT_NULL(careteam);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_CARETEAM, careteam->resource_type);
    
    FHIRResourceBase* goal = fhir_resource_create_by_name("Goal", "goal-789");
    ASSERT_NOT_NULL(goal);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_GOAL, goal->resource_type);
    
    FHIRResourceBase* service_request = fhir_resource_create_by_name("ServiceRequest", "req-101");
    ASSERT_NOT_NULL(service_request);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_SERVICEREQUEST, service_request->resource_type);
    
    FHIRResourceBase* nutrition_order = fhir_resource_create_by_name("NutritionOrder", "nutr-202");
    ASSERT_NOT_NULL(nutrition_order);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_NUTRITIONORDER, nutrition_order->resource_type);
    
    FHIRResourceBase* risk_assessment = fhir_resource_create_by_name("RiskAssessment", "risk-303");
    ASSERT_NOT_NULL(risk_assessment);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_RISKASSESSMENT, risk_assessment->resource_type);
    
    FHIRResourceBase* vision_prescription = fhir_resource_create_by_name("VisionPrescription", "vision-404");
    ASSERT_NOT_NULL(vision_prescription);
    ASSERT_EQ(FHIR_RESOURCE_TYPE_VISIONPRESCRIPTION, vision_prescription->resource_type);
    
    // Cleanup
    fhir_resource_release(careplan);
    fhir_resource_release(careteam);
    fhir_resource_release(goal);
    fhir_resource_release(service_request);
    fhir_resource_release(nutrition_order);
    fhir_resource_release(risk_assessment);
    fhir_resource_release(vision_prescription);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Care Provision Polymorphic Behavior                                 */
/* ========================================================================== */

bool test_care_provision_polymorphic_behavior(void) {
    TEST_START("Care Provision Polymorphic Behavior");
    
    // Create different Care Provision resource types
    FHIRResourceBase* resources[] = {
        fhir_resource_create_by_name("CarePlan", "plan-123"),
        fhir_resource_create_by_name("CareTeam", "team-456"),
        fhir_resource_create_by_name("Goal", "goal-789"),
        fhir_resource_create_by_name("ServiceRequest", "req-101"),
        fhir_resource_create_by_name("NutritionOrder", "nutr-202"),
        fhir_resource_create_by_name("RiskAssessment", "risk-303"),
        fhir_resource_create_by_name("VisionPrescription", "vision-404")
    };
    
    const char* expected_types[] = {
        "CarePlan", "CareTeam", "Goal", "ServiceRequest", 
        "NutritionOrder", "RiskAssessment", "VisionPrescription"
    };
    
    size_t resource_count = sizeof(resources) / sizeof(resources[0]);
    
    // Test polymorphic method calls
    for (size_t i = 0; i < resource_count; i++) {
        FHIRResourceBase* resource = resources[i];
        ASSERT_NOT_NULL(resource);
        
        // Test virtual method dispatch
        ASSERT_TRUE(fhir_resource_validate(resource));
        
        cJSON* json = fhir_resource_to_json(resource);
        ASSERT_NOT_NULL(json);
        
        const char* resource_type = fhir_json_get_string(json, "resourceType");
        ASSERT_STR_EQ(expected_types[i], resource_type);
        
        const char* display_name = fhir_resource_get_display_name(resource);
        ASSERT_NOT_NULL(display_name);
        
        // Test cloning
        FHIRResourceBase* clone = fhir_resource_clone(resource);
        ASSERT_NOT_NULL(clone);
        ASSERT_EQ(resource->resource_type, clone->resource_type);
        ASSERT_STR_EQ(resource->id, clone->id);
        ASSERT_NE(resource, clone);
        
        cJSON_Delete(json);
        fhir_resource_release(clone);
    }
    
    // Cleanup
    for (size_t i = 0; i < resource_count; i++) {
        fhir_resource_release(resources[i]);
    }
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Care Provision JSON Serialization                                   */
/* ========================================================================== */

bool test_care_provision_json_serialization(void) {
    TEST_START("Care Provision JSON Serialization");
    
    // Test CarePlan JSON serialization
    FHIRCarePlan* careplan = fhir_careplan_create("plan-123");
    ASSERT_NOT_NULL(careplan);
    
    fhir_careplan_set_status(careplan, FHIR_CAREPLAN_STATUS_ACTIVE);
    fhir_careplan_set_intent(careplan, FHIR_CAREPLAN_INTENT_PLAN);
    
    cJSON* json = fhir_careplan_to_json(careplan);
    ASSERT_NOT_NULL(json);
    
    const char* status = fhir_json_get_string(json, "status");
    ASSERT_STR_EQ("active", status);
    
    const char* intent = fhir_json_get_string(json, "intent");
    ASSERT_STR_EQ("plan", intent);
    
    cJSON_Delete(json);
    fhir_careplan_destroy(careplan);
    
    // Test RiskAssessment JSON serialization
    FHIRRiskAssessment* assessment = fhir_riskassessment_create("risk-456");
    ASSERT_NOT_NULL(assessment);
    
    fhir_riskassessment_set_status(assessment, FHIR_RISKASSESSMENT_STATUS_FINAL);
    
    json = fhir_riskassessment_to_json(assessment);
    ASSERT_NOT_NULL(json);
    
    status = fhir_json_get_string(json, "status");
    ASSERT_STR_EQ("final", status);
    
    cJSON_Delete(json);
    fhir_riskassessment_destroy(assessment);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Test Care Provision Resource Validation                                   */
/* ========================================================================== */

bool test_care_provision_validation(void) {
    TEST_START("Care Provision Resource Validation");
    
    // Test CarePlan validation
    FHIRCarePlan* careplan = fhir_careplan_create("plan-123");
    ASSERT_NOT_NULL(careplan);
    
    // Without subject, validation should fail
    ASSERT_FALSE(fhir_careplan_validate(careplan));
    
    // Add required subject
    careplan->subject = fhir_reference_create();
    ASSERT_NOT_NULL(careplan->subject);
    careplan->subject->reference = fhir_string_create("Patient/patient-123");
    
    // Now validation should pass
    ASSERT_TRUE(fhir_careplan_validate(careplan));
    
    fhir_careplan_destroy(careplan);
    
    // Test RiskAssessment validation
    FHIRRiskAssessment* assessment = fhir_riskassessment_create("risk-456");
    ASSERT_NOT_NULL(assessment);
    
    // Without subject, validation should fail
    ASSERT_FALSE(fhir_riskassessment_validate(assessment));
    
    // Add required subject
    assessment->subject = fhir_reference_create();
    ASSERT_NOT_NULL(assessment->subject);
    assessment->subject->reference = fhir_string_create("Patient/patient-456");
    
    // Now validation should pass
    ASSERT_TRUE(fhir_riskassessment_validate(assessment));
    
    fhir_riskassessment_destroy(assessment);
    
    TEST_PASS();
}

/* ========================================================================== */
/* Main Test Runner                                                          */
/* ========================================================================== */

int main(void) {
    TEST_INIT();
    
    printf("Running Care Provision Resources Tests...\n\n");
    
    // CarePlan tests
    RUN_TEST(test_careplan_creation_and_polymorphism);
    RUN_TEST(test_careplan_status_conversion);
    
    // RiskAssessment tests
    RUN_TEST(test_riskassessment_creation_and_functionality);
    RUN_TEST(test_riskassessment_status_conversion);
    
    // Factory and polymorphism tests
    RUN_TEST(test_care_provision_factory_registration);
    RUN_TEST(test_care_provision_polymorphic_behavior);
    
    // Serialization and validation tests
    RUN_TEST(test_care_provision_json_serialization);
    RUN_TEST(test_care_provision_validation);
    
    TEST_FINALIZE();
    
    return 0;
}