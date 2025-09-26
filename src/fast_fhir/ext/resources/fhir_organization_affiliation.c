/**
 * @file fhir_organization_affiliation.c
 * @brief FHIR R5 OrganizationAffiliation resource C implementation
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * Implementation of FHIR R5 OrganizationAffiliation resource following
 * C99 standards and best practices for memory management and error handling.
 */

#include "fhir_organization_affiliation.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

/* ========================================================================== */
/* Private Helper Functions                                                   */
/* ========================================================================== */

/**
 * @brief Initialize base domain resource fields
 * @param org_affiliation Target OrganizationAffiliation
 * @param id Resource identifier
 * @return true on success, false on failure
 */
static bool init_base_resource(FHIROrganizationAffiliation* org_affiliation, const char* id) {
    if (!org_affiliation || !id) {
        return false;
    }
    
    // Initialize base domain resource
    org_affiliation->domain_resource.resource.resource_type = strdup("OrganizationAffiliation");
    if (!org_affiliation->domain_resource.resource.resource_type) {
        return false;
    }
    
    org_affiliation->domain_resource.resource.id = strdup(id);
    if (!org_affiliation->domain_resource.resource.id) {
        free(org_affiliation->domain_resource.resource.resource_type);
        return false;
    }
    
    return true;
}

/**
 * @brief Free array of references
 * @param references Array of references to free
 * @param count Number of references
 */
static void free_reference_array(FHIRReference** references, size_t count) {
    if (!references) return;
    
    for (size_t i = 0; i < count; i++) {
        if (references[i]) {
            // Free FHIRReference structure (implementation depends on FHIRReference definition)
            free(references[i]);
        }
    }
    free(references);
}

/**
 * @brief Free array of codeable concepts
 * @param concepts Array of codeable concepts to free
 * @param count Number of concepts
 */
static void free_codeable_concept_array(FHIRCodeableConcept** concepts, size_t count) {
    if (!concepts) return;
    
    for (size_t i = 0; i < count; i++) {
        if (concepts[i]) {
            // Free FHIRCodeableConcept structure (implementation depends on definition)
            free(concepts[i]);
        }
    }
    free(concepts);
}

/**
 * @brief Resize array with proper error handling
 * @param array Pointer to array pointer
 * @param old_size Current size
 * @param new_size New size
 * @param element_size Size of each element
 * @return true on success, false on failure
 */
static bool resize_array(void** array, size_t old_size, size_t new_size, size_t element_size) {
    if (new_size == 0) {
        free(*array);
        *array = NULL;
        return true;
    }
    
    void* new_array = realloc(*array, new_size * element_size);
    if (!new_array) {
        return false;
    }
    
    *array = new_array;
    
    // Initialize new elements to NULL
    if (new_size > old_size) {
        memset((char*)*array + (old_size * element_size), 0, 
               (new_size - old_size) * element_size);
    }
    
    return true;
}

/* ========================================================================== */
/* Public API Implementation                                                  */
/* ========================================================================== */

FHIROrganizationAffiliation* fhir_organization_affiliation_create(const char* id) {
    if (!id || strlen(id) == 0) {
        errno = EINVAL;
        return NULL;
    }
    
    FHIROrganizationAffiliation* org_affiliation = calloc(1, sizeof(FHIROrganizationAffiliation));
    if (!org_affiliation) {
        errno = ENOMEM;
        return NULL;
    }
    
    if (!init_base_resource(org_affiliation, id)) {
        free(org_affiliation);
        errno = ENOMEM;
        return NULL;
    }
    
    return org_affiliation;
}

void fhir_organization_affiliation_free(FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) {
        return;
    }
    
    // Free base resource fields
    free(org_affiliation->domain_resource.resource.resource_type);
    free(org_affiliation->domain_resource.resource.id);
    
    // Free OrganizationAffiliation-specific fields
    if (org_affiliation->identifier) {
        for (size_t i = 0; i < org_affiliation->identifier_count; i++) {
            if (org_affiliation->identifier[i]) {
                // Free FHIRIdentifier (implementation depends on structure)
                free(org_affiliation->identifier[i]);
            }
        }
        free(org_affiliation->identifier);
    }
    
    // Free boolean field
    free(org_affiliation->active);
    
    // Free period
    free(org_affiliation->period);
    
    // Free references
    free(org_affiliation->organization);
    free(org_affiliation->participating_organization);
    
    // Free arrays
    free_codeable_concept_array(org_affiliation->network, org_affiliation->network_count);
    free_codeable_concept_array(org_affiliation->code, org_affiliation->code_count);
    free_codeable_concept_array(org_affiliation->specialty, org_affiliation->specialty_count);
    free_reference_array(org_affiliation->location, org_affiliation->location_count);
    free_reference_array(org_affiliation->healthcare_service, org_affiliation->healthcare_service_count);
    free_reference_array(org_affiliation->endpoint, org_affiliation->endpoint_count);
    
    // Free telecom array
    if (org_affiliation->telecom) {
        for (size_t i = 0; i < org_affiliation->telecom_count; i++) {
            free(org_affiliation->telecom[i]);
        }
        free(org_affiliation->telecom);
    }
    
    free(org_affiliation);
}

FHIROrganizationAffiliation* fhir_organization_affiliation_parse(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) {
        errno = EINVAL;
        return NULL;
    }
    
    // Get and validate resource type
    cJSON* resource_type_json = cJSON_GetObjectItem(json, "resourceType");
    if (!resource_type_json || !cJSON_IsString(resource_type_json) ||
        strcmp(resource_type_json->valuestring, "OrganizationAffiliation") != 0) {
        errno = EINVAL;
        return NULL;
    }
    
    // Get ID
    cJSON* id_json = cJSON_GetObjectItem(json, "id");
    if (!id_json || !cJSON_IsString(id_json)) {
        errno = EINVAL;
        return NULL;
    }
    
    FHIROrganizationAffiliation* org_affiliation = fhir_organization_affiliation_create(id_json->valuestring);
    if (!org_affiliation) {
        return NULL;
    }
    
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
    if (org_json && cJSON_IsObject(org_json)) {
        org_affiliation->organization = malloc(sizeof(FHIRReference));
        if (org_affiliation->organization) {
            // Parse reference fields (implementation depends on FHIRReference structure)
            cJSON* reference_json = cJSON_GetObjectItem(org_json, "reference");
            if (reference_json && cJSON_IsString(reference_json)) {
                // Store reference string (simplified implementation)
                // In full implementation, would parse all FHIRReference fields
            }
        }
    }
    
    // Parse participating organization reference
    cJSON* participating_org_json = cJSON_GetObjectItem(json, "participatingOrganization");
    if (participating_org_json && cJSON_IsObject(participating_org_json)) {
        org_affiliation->participating_organization = malloc(sizeof(FHIRReference));
        if (org_affiliation->participating_organization) {
            // Parse reference fields (implementation depends on FHIRReference structure)
        }
    }
    
    // Parse arrays (network, code, specialty, etc.)
    // Implementation would continue for all fields...
    
    return org_affiliation;
}

cJSON* fhir_organization_affiliation_to_json(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) {
        errno = EINVAL;
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        errno = ENOMEM;
        return NULL;
    }
    
    // Add resource type and id
    if (!cJSON_AddStringToObject(json, "resourceType", "OrganizationAffiliation") ||
        !cJSON_AddStringToObject(json, "id", org_affiliation->domain_resource.resource.id)) {
        cJSON_Delete(json);
        errno = ENOMEM;
        return NULL;
    }
    
    // Add active field
    if (org_affiliation->active) {
        if (!cJSON_AddBoolToObject(json, "active", org_affiliation->active->value)) {
            cJSON_Delete(json);
            errno = ENOMEM;
            return NULL;
        }
    }
    
    // Add organization reference
    if (org_affiliation->organization) {
        cJSON* org_json = cJSON_CreateObject();
        if (!org_json) {
            cJSON_Delete(json);
            errno = ENOMEM;
            return NULL;
        }
        
        // Add reference fields (implementation depends on FHIRReference structure)
        // Simplified implementation
        cJSON_AddItemToObject(json, "organization", org_json);
    }
    
    // Add participating organization reference
    if (org_affiliation->participating_organization) {
        cJSON* participating_org_json = cJSON_CreateObject();
        if (!participating_org_json) {
            cJSON_Delete(json);
            errno = ENOMEM;
            return NULL;
        }
        
        cJSON_AddItemToObject(json, "participatingOrganization", participating_org_json);
    }
    
    // Add arrays (network, code, specialty, etc.)
    // Implementation would continue for all fields...
    
    return json;
}

bool fhir_organization_affiliation_validate(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) {
        return false;
    }
    
    // Validate required fields according to FHIR R5 specification
    if (!org_affiliation->organization) {
        return false;
    }
    
    if (!org_affiliation->participating_organization) {
        return false;
    }
    
    // Additional validation rules can be added here
    
    return true;
}

bool fhir_organization_affiliation_is_active(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation || !org_affiliation->active) {
        return false;
    }
    
    return org_affiliation->active->value;
}

bool fhir_organization_affiliation_add_network(FHIROrganizationAffiliation* org_affiliation, 
                                              const FHIRCodeableConcept* network) {
    if (!org_affiliation || !network) {
        errno = EINVAL;
        return false;
    }
    
    // Resize network array
    if (!resize_array((void**)&org_affiliation->network, 
                     org_affiliation->network_count,
                     org_affiliation->network_count + 1,
                     sizeof(FHIRCodeableConcept*))) {
        errno = ENOMEM;
        return false;
    }
    
    // Allocate and copy network
    org_affiliation->network[org_affiliation->network_count] = malloc(sizeof(FHIRCodeableConcept));
    if (!org_affiliation->network[org_affiliation->network_count]) {
        errno = ENOMEM;
        return false;
    }
    
    // Copy network data (implementation depends on FHIRCodeableConcept structure)
    memcpy(org_affiliation->network[org_affiliation->network_count], network, sizeof(FHIRCodeableConcept));
    org_affiliation->network_count++;
    
    return true;
}

bool fhir_organization_affiliation_add_specialty(FHIROrganizationAffiliation* org_affiliation, 
                                                const FHIRCodeableConcept* specialty) {
    if (!org_affiliation || !specialty) {
        errno = EINVAL;
        return false;
    }
    
    // Similar implementation to add_network
    if (!resize_array((void**)&org_affiliation->specialty, 
                     org_affiliation->specialty_count,
                     org_affiliation->specialty_count + 1,
                     sizeof(FHIRCodeableConcept*))) {
        errno = ENOMEM;
        return false;
    }
    
    org_affiliation->specialty[org_affiliation->specialty_count] = malloc(sizeof(FHIRCodeableConcept));
    if (!org_affiliation->specialty[org_affiliation->specialty_count]) {
        errno = ENOMEM;
        return false;
    }
    
    memcpy(org_affiliation->specialty[org_affiliation->specialty_count], specialty, sizeof(FHIRCodeableConcept));
    org_affiliation->specialty_count++;
    
    return true;
}

bool fhir_organization_affiliation_add_location(FHIROrganizationAffiliation* org_affiliation, 
                                               const FHIRReference* location) {
    if (!org_affiliation || !location) {
        errno = EINVAL;
        return false;
    }
    
    // Similar implementation to add_network
    if (!resize_array((void**)&org_affiliation->location, 
                     org_affiliation->location_count,
                     org_affiliation->location_count + 1,
                     sizeof(FHIRReference*))) {
        errno = ENOMEM;
        return false;
    }
    
    org_affiliation->location[org_affiliation->location_count] = malloc(sizeof(FHIRReference));
    if (!org_affiliation->location[org_affiliation->location_count]) {
        errno = ENOMEM;
        return false;
    }
    
    memcpy(org_affiliation->location[org_affiliation->location_count], location, sizeof(FHIRReference));
    org_affiliation->location_count++;
    
    return true;
}

const FHIRReference* fhir_organization_affiliation_get_organization(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) {
        return NULL;
    }
    
    return org_affiliation->organization;
}

const FHIRReference* fhir_organization_affiliation_get_participating_organization(const FHIROrganizationAffiliation* org_affiliation) {
    if (!org_affiliation) {
        return NULL;
    }
    
    return org_affiliation->participating_organization;
}