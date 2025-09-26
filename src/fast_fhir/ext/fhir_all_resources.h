#ifndef FHIR_ALL_RESOURCES_H
#define FHIR_ALL_RESOURCES_H

// Master header file for all FHIR R5 resource types
// Based on https://www.hl7.org/fhir/resourcelist.html

#include "fhir_datatypes.h"
#include "fhir_foundation.h"
#include "fhir_clinical.h"
#include "fhir_medication.h"
#include "fhir_workflow.h"
#include "fhir_specialized.h"
#include "fhir_financial.h"

// Complete FHIR R5 Resource Type Registry
typedef enum {
    // Foundation Resources (Base)
    FHIR_RESOURCE_PATIENT,
    FHIR_RESOURCE_PRACTITIONER,
    FHIR_RESOURCE_PRACTITIONER_ROLE,
    FHIR_RESOURCE_ORGANIZATION,
    FHIR_RESOURCE_ORGANIZATION_AFFILIATION,
    FHIR_RESOURCE_LOCATION,
    FHIR_RESOURCE_HEALTHCARE_SERVICE,
    FHIR_RESOURCE_ENDPOINT,
    FHIR_RESOURCE_RELATED_PERSON,
    FHIR_RESOURCE_PERSON,
    FHIR_RESOURCE_GROUP,
    
    // Foundation Resources (Terminology)
    FHIR_RESOURCE_CODE_SYSTEM,
    FHIR_RESOURCE_VALUE_SET,
    FHIR_RESOURCE_CONCEPT_MAP,
    FHIR_RESOURCE_NAMING_SYSTEM,
    
    // Foundation Resources (Infrastructure)
    FHIR_RESOURCE_BINARY,
    FHIR_RESOURCE_BUNDLE,
    FHIR_RESOURCE_COMPOSITION,
    FHIR_RESOURCE_DOCUMENT_MANIFEST,
    FHIR_RESOURCE_DOCUMENT_REFERENCE,
    FHIR_RESOURCE_MESSAGE_DEFINITION,
    FHIR_RESOURCE_MESSAGE_HEADER,
    FHIR_RESOURCE_OPERATION_DEFINITION,
    FHIR_RESOURCE_OPERATION_OUTCOME,
    FHIR_RESOURCE_PARAMETERS,
    FHIR_RESOURCE_SUBSCRIPTION,
    FHIR_RESOURCE_SUBSCRIPTION_STATUS,
    FHIR_RESOURCE_SUBSCRIPTION_TOPIC,
    
    // Clinical Resources (Summary)
    FHIR_RESOURCE_ALLERGY_INTOLERANCE,
    FHIR_RESOURCE_CONDITION,
    FHIR_RESOURCE_PROCEDURE,
    FHIR_RESOURCE_FAMILY_MEMBER_HISTORY,
    FHIR_RESOURCE_CLINICAL_IMPRESSION,
    FHIR_RESOURCE_DETECTED_ISSUE,
    
    // Clinical Resources (Diagnostics)
    FHIR_RESOURCE_OBSERVATION,
    FHIR_RESOURCE_MEDIA,
    FHIR_RESOURCE_DIAGNOSTIC_REPORT,
    FHIR_RESOURCE_SPECIMEN,
    FHIR_RESOURCE_BODY_STRUCTURE,
    FHIR_RESOURCE_IMAGING_STUDY,
    FHIR_RESOURCE_IMAGING_SELECTION,
    FHIR_RESOURCE_MOLECULAR_SEQUENCE,
    
    // Clinical Resources (Care Provision)
    FHIR_RESOURCE_CARE_PLAN,
    FHIR_RESOURCE_CARE_TEAM,
    FHIR_RESOURCE_GOAL,
    FHIR_RESOURCE_SERVICE_REQUEST,
    FHIR_RESOURCE_NUTRITION_ORDER,
    FHIR_RESOURCE_RISK_ASSESSMENT,
    FHIR_RESOURCE_VISION_PRESCRIPTION,
    
    // Medication Resources
    FHIR_RESOURCE_MEDICATION,
    FHIR_RESOURCE_MEDICATION_ADMINISTRATION,
    FHIR_RESOURCE_MEDICATION_DISPENSE,
    FHIR_RESOURCE_MEDICATION_REQUEST,
    FHIR_RESOURCE_MEDICATION_STATEMENT,
    FHIR_RESOURCE_MEDICATION_KNOWLEDGE,
    FHIR_RESOURCE_IMMUNIZATION,
    FHIR_RESOURCE_IMMUNIZATION_EVALUATION,
    FHIR_RESOURCE_IMMUNIZATION_RECOMMENDATION,
    
    // Workflow Resources (Request & Response)
    FHIR_RESOURCE_APPOINTMENT,
    FHIR_RESOURCE_APPOINTMENT_RESPONSE,
    FHIR_RESOURCE_SCHEDULE,
    FHIR_RESOURCE_SLOT,
    FHIR_RESOURCE_ENCOUNTER,
    FHIR_RESOURCE_ENCOUNTER_HISTORY,
    FHIR_RESOURCE_EPISODE_OF_CARE,
    FHIR_RESOURCE_FLAG,
    FHIR_RESOURCE_LIST,
    FHIR_RESOURCE_LIBRARY,
    FHIR_RESOURCE_TASK,
    FHIR_RESOURCE_TRANSPORT,
    
    // Workflow Resources (Definition)
    FHIR_RESOURCE_ACTIVITY_DEFINITION,
    FHIR_RESOURCE_PLAN_DEFINITION,
    FHIR_RESOURCE_QUESTIONNAIRE,
    FHIR_RESOURCE_QUESTIONNAIRE_RESPONSE,
    
    // Financial Resources (Support)
    FHIR_RESOURCE_COVERAGE,
    FHIR_RESOURCE_COVERAGE_ELIGIBILITY_REQUEST,
    FHIR_RESOURCE_COVERAGE_ELIGIBILITY_RESPONSE,
    FHIR_RESOURCE_ENROLLMENT_REQUEST,
    FHIR_RESOURCE_ENROLLMENT_RESPONSE,
    
    // Financial Resources (Billing)
    FHIR_RESOURCE_ACCOUNT,
    FHIR_RESOURCE_CHARGE_ITEM,
    FHIR_RESOURCE_CHARGE_ITEM_DEFINITION,
    FHIR_RESOURCE_CONTRACT,
    FHIR_RESOURCE_INVOICE,
    
    // Financial Resources (Payment)
    FHIR_RESOURCE_PAYMENT_NOTICE,
    FHIR_RESOURCE_PAYMENT_RECONCILIATION,
    
    // Financial Resources (General)
    FHIR_RESOURCE_CLAIM,
    FHIR_RESOURCE_CLAIM_RESPONSE,
    FHIR_RESOURCE_EXPLANATION_OF_BENEFIT,
    
    // Specialized Resources (Public Health & Research)
    FHIR_RESOURCE_RESEARCH_STUDY,
    FHIR_RESOURCE_RESEARCH_SUBJECT,
    FHIR_RESOURCE_ADVERSE_EVENT,
    
    // Specialized Resources (Definitional Artifacts)
    FHIR_RESOURCE_EVIDENCE,
    FHIR_RESOURCE_EVIDENCE_REPORT,
    FHIR_RESOURCE_EVIDENCE_VARIABLE,
    FHIR_RESOURCE_CITATION,
    
    // Specialized Resources (Quality Reporting & Testing)
    FHIR_RESOURCE_MEASURE,
    FHIR_RESOURCE_MEASURE_REPORT,
    FHIR_RESOURCE_TEST_REPORT,
    FHIR_RESOURCE_TEST_SCRIPT,
    
    // Specialized Resources (Medication Definition)
    FHIR_RESOURCE_SUBSTANCE,
    FHIR_RESOURCE_SUBSTANCE_DEFINITION,
    FHIR_RESOURCE_SUBSTANCE_NUCLEIC_ACID,
    FHIR_RESOURCE_SUBSTANCE_POLYMER,
    FHIR_RESOURCE_SUBSTANCE_PROTEIN,
    FHIR_RESOURCE_SUBSTANCE_REFERENCE_INFORMATION,
    FHIR_RESOURCE_SUBSTANCE_SOURCE_MATERIAL,
    FHIR_RESOURCE_BIOLOGICALLY_DERIVED_PRODUCT,
    FHIR_RESOURCE_NUTRITION_PRODUCT,
    
    // Specialized Resources (Devices)
    FHIR_RESOURCE_DEVICE,
    FHIR_RESOURCE_DEVICE_DEFINITION,
    FHIR_RESOURCE_DEVICE_METRIC,
    FHIR_RESOURCE_DEVICE_REQUEST,
    FHIR_RESOURCE_DEVICE_USAGE,
    
    // Specialized Resources (Conformance)
    FHIR_RESOURCE_CAPABILITY_STATEMENT,
    FHIR_RESOURCE_STRUCTURE_DEFINITION,
    FHIR_RESOURCE_STRUCTURE_MAP,
    FHIR_RESOURCE_IMPLEMENTATION_GUIDE,
    FHIR_RESOURCE_SEARCH_PARAMETER,
    FHIR_RESOURCE_COMPARTMENT_DEFINITION,
    FHIR_RESOURCE_EXAMPLE_SCENARIO,
    FHIR_RESOURCE_GRAPH_DEFINITION,
    
    // Specialized Resources (Terminology)
    FHIR_RESOURCE_TERMINOLOGY_CAPABILITIES,
    
    // Specialized Resources (Security)
    FHIR_RESOURCE_AUDIT_EVENT,
    FHIR_RESOURCE_PROVENANCE,
    FHIR_RESOURCE_CONSENT,
    FHIR_RESOURCE_VERIFICATION_RESULT,
    
    // Specialized Resources (Documents)
    FHIR_RESOURCE_CATALOG_ENTRY,
    
    // Total count
    FHIR_RESOURCE_TYPE_COUNT
} FHIRResourceType;

// Resource type name mapping
extern const char* FHIR_RESOURCE_TYPE_NAMES[FHIR_RESOURCE_TYPE_COUNT];

// Resource category mapping
typedef enum {
    FHIR_CATEGORY_FOUNDATION,
    FHIR_CATEGORY_CLINICAL,
    FHIR_CATEGORY_MEDICATION,
    FHIR_CATEGORY_WORKFLOW,
    FHIR_CATEGORY_FINANCIAL,
    FHIR_CATEGORY_SPECIALIZED,
    FHIR_CATEGORY_UNKNOWN
} FHIRResourceCategory;

// Function declarations for resource type management
FHIRResourceType fhir_get_resource_type_enum(const char* resource_type_name);
const char* fhir_get_resource_type_name(FHIRResourceType resource_type);
FHIRResourceCategory fhir_get_resource_category(FHIRResourceType resource_type);
const char* fhir_get_resource_category_name(FHIRResourceCategory category);
bool fhir_is_valid_resource_type(const char* resource_type_name);

// Resource factory functions
FHIRResource* fhir_create_resource_by_type(FHIRResourceType resource_type, const char* id);
void fhir_free_resource_by_type(FHIRResource* resource, FHIRResourceType resource_type);
FHIRResource* fhir_parse_resource_by_type(cJSON* json, FHIRResourceType resource_type);
cJSON* fhir_resource_to_json_by_type(const FHIRResource* resource, FHIRResourceType resource_type);
bool fhir_validate_resource_by_type(const FHIRResource* resource, FHIRResourceType resource_type);

// Utility functions for all resources
bool fhir_resource_has_narrative(FHIRResourceType resource_type);
bool fhir_resource_has_contained(FHIRResourceType resource_type);
bool fhir_resource_has_extensions(FHIRResourceType resource_type);
const char** fhir_get_required_fields(FHIRResourceType resource_type);
const char** fhir_get_search_parameters(FHIRResourceType resource_type);

// Resource statistics and information
typedef struct {
    FHIRResourceType resource_type;
    size_t instance_count;
    size_t total_memory_usage;
    double average_parse_time_ms;
    double average_serialize_time_ms;
} FHIRResourceStats;

FHIRResourceStats* fhir_get_resource_stats(FHIRResourceType resource_type);
void fhir_reset_resource_stats(FHIRResourceType resource_type);
void fhir_print_all_resource_stats(void);

// Bulk operations
typedef struct {
    FHIRResource** resources;
    FHIRResourceType* resource_types;
    size_t count;
    size_t capacity;
} FHIRResourceCollection;

FHIRResourceCollection* fhir_resource_collection_create(size_t initial_capacity);
void fhir_resource_collection_free(FHIRResourceCollection* collection);
bool fhir_resource_collection_add(FHIRResourceCollection* collection, FHIRResource* resource, FHIRResourceType type);
FHIRResource* fhir_resource_collection_get(FHIRResourceCollection* collection, size_t index);
size_t fhir_resource_collection_filter_by_type(FHIRResourceCollection* collection, FHIRResourceType type, FHIRResource*** filtered_resources);

// Performance monitoring
typedef struct {
    double total_parse_time_ms;
    double total_serialize_time_ms;
    size_t total_resources_parsed;
    size_t total_resources_serialized;
    size_t peak_memory_usage_bytes;
    size_t current_memory_usage_bytes;
} FHIRPerformanceMetrics;

FHIRPerformanceMetrics* fhir_get_performance_metrics(void);
void fhir_reset_performance_metrics(void);
void fhir_start_performance_timer(void);
double fhir_stop_performance_timer(void);

#endif // FHIR_ALL_RESOURCES_H