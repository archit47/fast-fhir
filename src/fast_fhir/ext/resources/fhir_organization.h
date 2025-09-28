/**
 * @file fhir_organization.h
 * @brief FHIR R5 Organization resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * A formally or informally recognized grouping of people or organizations
 */

#ifndef FHIR_ORGANIZATION_H
#define FHIR_ORGANIZATION_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief FHIR R5 Organization resource structure
 * 
 * A formally or informally recognized grouping of people or organizations
 */
FHIR_RESOURCE_DEFINE(Organization)
    // Organization-specific fields
    FHIRBoolean* active;
    
    FHIRCodeableConcept** type;
    size_t type_count;
    
    FHIRString* name;
    
    FHIRString** alias;
    size_t alias_count;
    
    FHIRMarkdown* description;
    
    FHIRExtendedContactDetail** contact;
    size_t contact_count;
    
    FHIRReference* part_of;
    
    FHIRReference** endpoint;
    size_t endpoint_count;
    
    FHIROrganizationQualification** qualification;
    size_t qualification_count;
    
};

/* ========================================================================== */
/* Organization Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new Organization resource
 * @param id Resource identifier (required)
 * @return Pointer to new Organization or NULL on failure
 */
FHIROrganization* fhir_organization_create(const char* id);

/**
 * @brief Destroy Organization resource (virtual destructor)
 * @param self Organization to destroy
 */
void fhir_organization_destroy(FHIROrganization* self);

/**
 * @brief Clone Organization resource (virtual clone)
 * @param self Organization to clone
 * @return Cloned Organization or NULL on failure
 */
FHIROrganization* fhir_organization_clone(const FHIROrganization* self);

/* ========================================================================== */
/* Organization Serialization Methods                                     */
/* ========================================================================== */

/**
 * @brief Convert Organization to JSON (virtual method)
 * @param self Organization to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_organization_to_json(const FHIROrganization* self);

/**
 * @brief Load Organization from JSON (virtual method)
 * @param self Organization to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_organization_from_json(FHIROrganization* self, const cJSON* json);

/**
 * @brief Parse Organization from JSON string
 * @param json_string JSON string
 * @return New Organization or NULL on failure
 */
FHIROrganization* fhir_organization_parse(const char* json_string);

/* ========================================================================== */
/* Organization Validation Methods                                        */
/* ========================================================================== */

/**
 * @brief Validate Organization resource (virtual method)
 * @param self Organization to validate
 * @return true if valid, false otherwise
 */
bool fhir_organization_validate(const FHIROrganization* self);

/* ========================================================================== */
/* Organization-Specific Methods                                          */
/* ========================================================================== */

/**
 * @brief Check if Organization is active (virtual method)
 * @param self Organization to check
 * @return true if active, false otherwise
 */
bool fhir_organization_is_active(const FHIROrganization* self);

/**
 * @brief Get Organization display name (virtual method)
 * @param self Organization to get name from
 * @return Display name or NULL
 */
const char* fhir_organization_get_display_name(const FHIROrganization* self);

/**
 * @brief Register Organization resource type
 * @return true on success, false on failure
 */
bool fhir_organization_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_ORGANIZATION_H */