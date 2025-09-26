/**
 * @file fhir_organization_affiliation.h
 * @brief FHIR R5 OrganizationAffiliation resource C interface
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * This header defines the C interface for the FHIR R5 OrganizationAffiliation resource.
 * Follows FHIR R5 specification and C99 standards.
 */

#ifndef FHIR_ORGANIZATION_AFFILIATION_H
#define FHIR_ORGANIZATION_AFFILIATION_H

#include "../fhir_datatypes.h"
#include "../fhir_foundation.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief FHIR R5 OrganizationAffiliation resource structure
 * 
 * Defines a formal relationship between organizations where one organization
 * is affiliated with another organization.
 */
typedef struct FHIROrganizationAffiliation {
    /** Base domain resource */
    FHIRDomainResource domain_resource;
    
    /** Business identifiers that are known to this affiliation */
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    /** Whether this organization affiliation record is in active use */
    FHIRBoolean* active;
    
    /** The period during which the affiliation is/was active */
    FHIRPeriod* period;
    
    /** Organization where the role is available */
    FHIRReference* organization;
    
    /** Organization that provides/performs the role */
    FHIRReference* participating_organization;
    
    /** Health insurance provider network in which the role is performed */
    FHIRCodeableConcept** network;
    size_t network_count;
    
    /** Definition of the role the participatingOrganization plays */
    FHIRCodeableConcept** code;
    size_t code_count;
    
    /** Specific specialty of the participatingOrganization */
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    
    /** The location(s) at which the role occurs */
    FHIRReference** location;
    size_t location_count;
    
    /** Healthcare services provided through the affiliation */
    FHIRReference** healthcare_service;
    size_t healthcare_service_count;
    
    /** Contact details at the participatingOrganization relevant to this affiliation */
    FHIRContactPoint** telecom;
    size_t telecom_count;
    
    /** Technical endpoints providing access to services operated for this affiliation */
    FHIRReference** endpoint;
    size_t endpoint_count;
} FHIROrganizationAffiliation;

/**
 * @brief Create a new OrganizationAffiliation resource
 * @param id Resource identifier (required)
 * @return Pointer to new OrganizationAffiliation or NULL on failure
 * @note Caller is responsible for freeing the returned resource
 */
FHIROrganizationAffiliation* fhir_organization_affiliation_create(const char* id);

/**
 * @brief Free an OrganizationAffiliation resource and all its components
 * @param org_affiliation Pointer to OrganizationAffiliation to free (can be NULL)
 */
void fhir_organization_affiliation_free(FHIROrganizationAffiliation* org_affiliation);

/**
 * @brief Parse OrganizationAffiliation from JSON
 * @param json JSON object containing OrganizationAffiliation data
 * @return Pointer to parsed OrganizationAffiliation or NULL on failure
 */
FHIROrganizationAffiliation* fhir_organization_affiliation_parse(cJSON* json);

/**
 * @brief Convert OrganizationAffiliation to JSON
 * @param org_affiliation OrganizationAffiliation to convert
 * @return JSON object or NULL on failure
 * @note Caller is responsible for freeing the returned JSON object
 */
cJSON* fhir_organization_affiliation_to_json(const FHIROrganizationAffiliation* org_affiliation);

/**
 * @brief Validate OrganizationAffiliation resource
 * @param org_affiliation OrganizationAffiliation to validate
 * @return true if valid, false otherwise
 */
bool fhir_organization_affiliation_validate(const FHIROrganizationAffiliation* org_affiliation);

/**
 * @brief Check if OrganizationAffiliation is active
 * @param org_affiliation OrganizationAffiliation to check
 * @return true if active, false otherwise
 */
bool fhir_organization_affiliation_is_active(const FHIROrganizationAffiliation* org_affiliation);

/**
 * @brief Add a network to OrganizationAffiliation
 * @param org_affiliation Target OrganizationAffiliation
 * @param network Network to add
 * @return true on success, false on failure
 */
bool fhir_organization_affiliation_add_network(FHIROrganizationAffiliation* org_affiliation, 
                                              const FHIRCodeableConcept* network);

/**
 * @brief Add a specialty to OrganizationAffiliation
 * @param org_affiliation Target OrganizationAffiliation
 * @param specialty Specialty to add
 * @return true on success, false on failure
 */
bool fhir_organization_affiliation_add_specialty(FHIROrganizationAffiliation* org_affiliation, 
                                                const FHIRCodeableConcept* specialty);

/**
 * @brief Add a location to OrganizationAffiliation
 * @param org_affiliation Target OrganizationAffiliation
 * @param location Location reference to add
 * @return true on success, false on failure
 */
bool fhir_organization_affiliation_add_location(FHIROrganizationAffiliation* org_affiliation, 
                                               const FHIRReference* location);

/**
 * @brief Get the primary organization reference
 * @param org_affiliation OrganizationAffiliation to query
 * @return Primary organization reference or NULL
 */
const FHIRReference* fhir_organization_affiliation_get_organization(const FHIROrganizationAffiliation* org_affiliation);

/**
 * @brief Get the participating organization reference
 * @param org_affiliation OrganizationAffiliation to query
 * @return Participating organization reference or NULL
 */
const FHIRReference* fhir_organization_affiliation_get_participating_organization(const FHIROrganizationAffiliation* org_affiliation);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_ORGANIZATION_AFFILIATION_H */