/**
 * FHIR R5 New Resources C Implementation
 * 
 * This file contains C implementations for newly added FHIR resources:
 * - OrganizationAffiliation
 * - BiologicallyDerivedProduct
 * - DeviceMetric
 * - NutritionProduct
 * - Transport
 * - VerificationResult
 * - EncounterHistory
 * - EpisodeOfCare
 * 
 * Following DRY principles and best practices.
 */

#include "fhir_foundation.h"
#include "fhir_specialized.h"
#include "fhir_workflow.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// ============================================================================
// OrganizationAffiliation Implementation
// ============================================================================

FHIROrganizationAffiliation* fhir_organization_affiliation_create(const char* id) {
    if (!id) return NULL;
    
    FHIROrganizationAffiliation* org_affiliation = calloc(1, sizeof(FHIROrganizationAffiliation));
    if (!org_affiliation) return NULL;
    
    // Initialize base domain resource
    org_affiliation->domain_resource.resource.resource_type = strdup("OrganizationAffiliation");
    org_affiliation->domain_resource.resource.id = strdup(id);
    
    return org_affiliation;
}

void fhir_organization_affiliation_free(FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) return;
    
    // Free base resource fields
    free(org_affiliation->domain_resource.resource.resource_type);
    free(org_affiliation->domain_resource.resource.id);
    
    // Free OrganizationAffiliation-specific fields
    if (org_affiliation->identifier) {
        for (size_t i = 0; i < org_affiliation->identifier_count; i++) {
            // Free identifier (implementation depends on FHIRIdentifier structure)
        }
        free(org_affiliation->identifier);
    }
    
    // Free other arrays and structures
    free(org_affiliation->network);
    free(org_affiliation->code);
    free(org_affiliation->specialty);
    free(org_affiliation->location);
    free(org_affiliation->healthcare_service);
    free(org_affiliation->telecom);
    free(org_affiliation->endpoint);
    
    free(org_affiliation);
}

FHIROrganizationAffiliation* fhir_parse_organization_affiliation(cJSON* json) {
    if (!json) return NULL;
    
    cJSON* id_json = cJSON_GetObjectItem(json, "id");
    if (!id_json || !cJSON_IsString(id_json)) return NULL;
    
    FHIROrganizationAffiliation* org_affiliation = fhir_organization_affiliation_create(id_json->valuestring);
    if (!org_affiliation) return NULL;
    
    // Parse active field
    cJSON* active_json = cJSON_GetObjectItem(json, "active");
    if (active_json && cJSON_IsBool(active_json)) {
        org_affiliation->active = malloc(sizeof(FHIRBoolean));
        if (org_affiliation->active) {
            org_affiliation->active->value = cJSON_IsTrue(active_json);
        }
    }
    
    // Parse organization reference
    cJSON* org_json = cJSON_GetObjectItem(json, "organization");
    if (org_json) {
        // Parse reference (implementation depends on FHIRReference structure)
        org_affiliation->organization = malloc(sizeof(FHIRReference));
        // ... parse reference fields
    }
    
    // Parse participating organization reference
    cJSON* participating_org_json = cJSON_GetObjectItem(json, "participatingOrganization");
    if (participating_org_json) {
        org_affiliation->participating_organization = malloc(sizeof(FHIRReference));
        // ... parse reference fields
    }
    
    return org_affiliation;
}

cJSON* fhir_organization_affiliation_to_json(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    // Add resource type and id
    cJSON_AddStringToObject(json, "resourceType", "OrganizationAffiliation");
    if (org_affiliation->domain_resource.resource.id) {
        cJSON_AddStringToObject(json, "id", org_affiliation->domain_resource.resource.id);
    }
    
    // Add active field
    if (org_affiliation->active) {
        cJSON_AddBoolToObject(json, "active", org_affiliation->active->value);
    }
    
    // Add organization reference
    if (org_affiliation->organization) {
        cJSON* org_json = cJSON_CreateObject();
        // ... serialize reference fields
        cJSON_AddItemToObject(json, "organization", org_json);
    }
    
    // Add participating organization reference
    if (org_affiliation->participating_organization) {
        cJSON* participating_org_json = cJSON_CreateObject();
        // ... serialize reference fields
        cJSON_AddItemToObject(json, "participatingOrganization", participating_org_json);
    }
    
    return json;
}

bool fhir_validate_organization_affiliation(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) return false;
    
    // Validate required fields
    if (!org_affiliation->organization) return false;
    if (!org_affiliation->participating_organization) return false;
    
    return true;
}

// ============================================================================
// BiologicallyDerivedProduct Implementation
// ============================================================================

FHIRBiologicallyDerivedProduct* fhir_biologically_derived_product_create(const char* id) {
    if (!id) return NULL;
    
    FHIRBiologicallyDerivedProduct* product = calloc(1, sizeof(FHIRBiologicallyDerivedProduct));
    if (!product) return NULL;
    
    // Initialize base domain resource
    product->domain_resource.resource.resource_type = strdup("BiologicallyDerivedProduct");
    product->domain_resource.resource.id = strdup(id);
    
    return product;
}

void fhir_biologically_derived_product_free(FHIRBiologicallyDerivedProduct* product) {
    if (!product) return;
    
    // Free base resource fields
    free(product->domain_resource.resource.resource_type);
    free(product->domain_resource.resource.id);
    
    // Free BiologicallyDerivedProduct-specific fields
    if (product->identifier) {
        for (size_t i = 0; i < product->identifier_count; i++) {
            // Free identifier
        }
        free(product->identifier);
    }
    
    if (product->parent) {
        for (size_t i = 0; i < product->parent_count; i++) {
            // Free reference
        }
        free(product->parent);
    }
    
    if (product->processing) {
        for (size_t i = 0; i < product->processing_count; i++) {
            // Free processing structure
        }
        free(product->processing);
    }
    
    if (product->storage) {
        for (size_t i = 0; i < product->storage_count; i++) {
            // Free storage structure
        }
        free(product->storage);
    }
    
    free(product->biological_source_event);
    free(product->manipulation);
    
    free(product);
}

bool fhir_validate_biologically_derived_product(const FHIRBiologicallyDerivedProduct* product) {
    if (!product) return false;
    
    // Validate required fields
    if (!product->product_category) return false;
    
    return true;
}

// ============================================================================
// DeviceMetric Implementation
// ============================================================================

FHIRDeviceMetric* fhir_device_metric_create(const char* id) {
    if (!id) return NULL;
    
    FHIRDeviceMetric* metric = calloc(1, sizeof(FHIRDeviceMetric));
    if (!metric) return NULL;
    
    // Initialize base domain resource
    metric->domain_resource.resource.resource_type = strdup("DeviceMetric");
    metric->domain_resource.resource.id = strdup(id);
    
    return metric;
}

void fhir_device_metric_free(FHIRDeviceMetric* metric) {
    if (!metric) return;
    
    // Free base resource fields
    free(metric->domain_resource.resource.resource_type);
    free(metric->domain_resource.resource.id);
    
    // Free DeviceMetric-specific fields
    if (metric->identifier) {
        for (size_t i = 0; i < metric->identifier_count; i++) {
            // Free identifier
        }
        free(metric->identifier);
    }
    
    if (metric->calibration) {
        for (size_t i = 0; i < metric->calibration_count; i++) {
            // Free calibration structure
        }
        free(metric->calibration);
    }
    
    free(metric);
}

bool fhir_validate_device_metric(const FHIRDeviceMetric* metric) {
    if (!metric) return false;
    
    // Validate required fields
    if (!metric->type) return false;
    if (!metric->category) return false;
    
    return true;
}

// ============================================================================
// NutritionProduct Implementation
// ============================================================================

FHIRNutritionProduct* fhir_nutrition_product_create(const char* id) {
    if (!id) return NULL;
    
    FHIRNutritionProduct* product = calloc(1, sizeof(FHIRNutritionProduct));
    if (!product) return NULL;
    
    // Initialize base domain resource
    product->domain_resource.resource.resource_type = strdup("NutritionProduct");
    product->domain_resource.resource.id = strdup(id);
    
    return product;
}

void fhir_nutrition_product_free(FHIRNutritionProduct* product) {
    if (!product) return;
    
    // Free base resource fields
    free(product->domain_resource.resource.resource_type);
    free(product->domain_resource.resource.id);
    
    // Free NutritionProduct-specific fields
    if (product->category) {
        for (size_t i = 0; i < product->category_count; i++) {
            // Free category
        }
        free(product->category);
    }
    
    if (product->nutrient) {
        for (size_t i = 0; i < product->nutrient_count; i++) {
            // Free nutrient structure
        }
        free(product->nutrient);
    }
    
    if (product->ingredient) {
        for (size_t i = 0; i < product->ingredient_count; i++) {
            // Free ingredient structure
        }
        free(product->ingredient);
    }
    
    free(product->manufacturer);
    
    free(product);
}

bool fhir_validate_nutrition_product(const FHIRNutritionProduct* product) {
    if (!product) return false;
    
    // Validate required fields
    if (!product->status) return false;
    
    return true;
}

// ============================================================================
// Transport Implementation
// ============================================================================

FHIRTransport* fhir_transport_create(const char* id) {
    if (!id) return NULL;
    
    FHIRTransport* transport = calloc(1, sizeof(FHIRTransport));
    if (!transport) return NULL;
    
    // Initialize base domain resource
    transport->domain_resource.resource.resource_type = strdup("Transport");
    transport->domain_resource.resource.id = strdup(id);
    
    return transport;
}

void fhir_transport_free(FHIRTransport* transport) {
    if (!transport) return;
    
    // Free base resource fields
    free(transport->domain_resource.resource.resource_type);
    free(transport->domain_resource.resource.id);
    
    // Free Transport-specific fields
    if (transport->identifier) {
        for (size_t i = 0; i < transport->identifier_count; i++) {
            // Free identifier
        }
        free(transport->identifier);
    }
    
    free(transport->instantiates_canonical);
    free(transport->instantiates_uri);
    free(transport->description);
    
    free(transport);
}

bool fhir_validate_transport(const FHIRTransport* transport) {
    if (!transport) return false;
    
    // Validate required fields
    if (!transport->status) return false;
    if (!transport->intent) return false;
    
    return true;
}

// ============================================================================
// VerificationResult Implementation
// ============================================================================

FHIRVerificationResult* fhir_verification_result_create(const char* id) {
    if (!id) return NULL;
    
    FHIRVerificationResult* result = calloc(1, sizeof(FHIRVerificationResult));
    if (!result) return NULL;
    
    // Initialize base domain resource
    result->domain_resource.resource.resource_type = strdup("VerificationResult");
    result->domain_resource.resource.id = strdup(id);
    
    return result;
}

void fhir_verification_result_free(FHIRVerificationResult* result) {
    if (!result) return;
    
    // Free base resource fields
    free(result->domain_resource.resource.resource_type);
    free(result->domain_resource.resource.id);
    
    // Free VerificationResult-specific fields
    if (result->target) {
        for (size_t i = 0; i < result->target_count; i++) {
            // Free reference
        }
        free(result->target);
    }
    
    if (result->target_location) {
        for (size_t i = 0; i < result->target_location_count; i++) {
            free(result->target_location[i]);
        }
        free(result->target_location);
    }
    
    free(result);
}

bool fhir_validate_verification_result(const FHIRVerificationResult* result) {
    if (!result) return false;
    
    // Validate required fields
    if (!result->target || result->target_count == 0) return false;
    if (!result->status) return false;
    
    return true;
}

// ============================================================================
// EncounterHistory Implementation
// ============================================================================

FHIREncounterHistory* fhir_encounter_history_create(const char* id) {
    if (!id) return NULL;
    
    FHIREncounterHistory* history = calloc(1, sizeof(FHIREncounterHistory));
    if (!history) return NULL;
    
    // Initialize base domain resource
    history->domain_resource.resource.resource_type = strdup("EncounterHistory");
    history->domain_resource.resource.id = strdup(id);
    
    return history;
}

void fhir_encounter_history_free(FHIREncounterHistory* history) {
    if (!history) return;
    
    // Free base resource fields
    free(history->domain_resource.resource.resource_type);
    free(history->domain_resource.resource.id);
    
    // Free EncounterHistory-specific fields
    if (history->identifier) {
        for (size_t i = 0; i < history->identifier_count; i++) {
            // Free identifier
        }
        free(history->identifier);
    }
    
    if (history->service_type) {
        for (size_t i = 0; i < history->service_type_count; i++) {
            // Free service type
        }
        free(history->service_type);
    }
    
    if (history->location) {
        for (size_t i = 0; i < history->location_count; i++) {
            // Free location structure
        }
        free(history->location);
    }
    
    free(history);
}

bool fhir_validate_encounter_history(const FHIREncounterHistory* history) {
    if (!history) return false;
    
    // Validate required fields
    if (!history->status) return false;
    if (!history->class) return false;
    if (!history->subject) return false;
    if (!history->encounter) return false;
    
    return true;
}

// ============================================================================
// EpisodeOfCare Implementation
// ============================================================================

FHIREpisodeOfCare* fhir_episode_of_care_create(const char* id) {
    if (!id) return NULL;
    
    FHIREpisodeOfCare* episode = calloc(1, sizeof(FHIREpisodeOfCare));
    if (!episode) return NULL;
    
    // Initialize base domain resource
    episode->domain_resource.resource.resource_type = strdup("EpisodeOfCare");
    episode->domain_resource.resource.id = strdup(id);
    
    return episode;
}

void fhir_episode_of_care_free(FHIREpisodeOfCare* episode) {
    if (!episode) return;
    
    // Free base resource fields
    free(episode->domain_resource.resource.resource_type);
    free(episode->domain_resource.resource.id);
    
    // Free EpisodeOfCare-specific fields
    if (episode->identifier) {
        for (size_t i = 0; i < episode->identifier_count; i++) {
            // Free identifier
        }
        free(episode->identifier);
    }
    
    if (episode->status_history) {
        for (size_t i = 0; i < episode->status_history_count; i++) {
            // Free status history structure
        }
        free(episode->status_history);
    }
    
    if (episode->diagnosis) {
        for (size_t i = 0; i < episode->diagnosis_count; i++) {
            // Free diagnosis structure
        }
        free(episode->diagnosis);
    }
    
    free(episode);
}

bool fhir_validate_episode_of_care(const FHIREpisodeOfCare* episode) {
    if (!episode) return false;
    
    // Validate required fields
    if (!episode->status) return false;
    if (!episode->patient) return false;
    
    return true;
}

// ============================================================================
// Utility Functions
// ============================================================================

bool fhir_is_active_nutrition_product(const FHIRNutritionProduct* product) {
    if (!product || !product->status) return false;
    return strcmp(product->status->value, "active") == 0;
}

bool fhir_is_validated_verification_result(const FHIRVerificationResult* result) {
    if (!result || !result->status) return false;
    return strcmp(result->status->value, "validated") == 0;
}