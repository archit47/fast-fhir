/**
 * @file fhir_practitionerrole.h
 * @brief FHIR R5 PractitionerRole resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * A specific set of Roles/Locations/specialties/services that a practitioner may perform
 */

#ifndef FHIR_PRACTITIONERROLE_H
#define FHIR_PRACTITIONERROLE_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief PractitionerRole active_status enumeration
 */
typedef enum {
    FHIRPRACTITIONERROLEACTIVESTATUS_ACTIVE = 0,
    FHIRPRACTITIONERROLEACTIVESTATUS_INACTIVE = 1,
} FHIRPractitionerRoleActiveStatus;

/**
 * @brief FHIR R5 PractitionerRole resource structure
 * 
 * A specific set of Roles/Locations/specialties/services that a practitioner may perform
 */
FHIR_RESOURCE_DEFINE(PractitionerRole)
    // PractitionerRole-specific fields
    FHIRBoolean* active;
    
    FHIRPeriod* period;
    
    FHIRReference* practitioner;
    
    FHIRReference* organization;
    
    FHIRCodeableConcept** code;
    size_t code_count;
    
    FHIRCodeableConcept** specialty;
    size_t specialty_count;
    
    FHIRReference** location;
    size_t location_count;
    
    FHIRReference** healthcare_service;
    size_t healthcare_service_count;
    
    FHIRExtendedContactDetail** contact;
    size_t contact_count;
    
    FHIRCodeableConcept** characteristic;
    size_t characteristic_count;
    
    FHIRCodeableConcept** communication;
    size_t communication_count;
    
    FHIRAvailability** availability;
    size_t availability_count;
    
    FHIRReference** endpoint;
    size_t endpoint_count;
    
};

/* ========================================================================== */
/* PractitionerRole Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new PractitionerRole resource
 * @param id Resource identifier (required)
 * @return Pointer to new PractitionerRole or NULL on failure
 */
FHIRPractitionerRole* fhir_practitionerrole_create(const char* id);

/**
 * @brief Destroy PractitionerRole resource (virtual destructor)
 * @param self PractitionerRole to destroy
 */
void fhir_practitionerrole_destroy(FHIRPractitionerRole* self);

/**
 * @brief Clone PractitionerRole resource (virtual clone)
 * @param self PractitionerRole to clone
 * @return Cloned PractitionerRole or NULL on failure
 */
FHIRPractitionerRole* fhir_practitionerrole_clone(const FHIRPractitionerRole* self);

/* ========================================================================== */
/* PractitionerRole Serialization Methods                                     */
/* ========================================================================== */

/**
 * @brief Convert PractitionerRole to JSON (virtual method)
 * @param self PractitionerRole to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_practitionerrole_to_json(const FHIRPractitionerRole* self);

/**
 * @brief Load PractitionerRole from JSON (virtual method)
 * @param self PractitionerRole to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_practitionerrole_from_json(FHIRPractitionerRole* self, const cJSON* json);

/**
 * @brief Parse PractitionerRole from JSON string
 * @param json_string JSON string
 * @return New PractitionerRole or NULL on failure
 */
FHIRPractitionerRole* fhir_practitionerrole_parse(const char* json_string);

/* ========================================================================== */
/* PractitionerRole Validation Methods                                        */
/* ========================================================================== */

/**
 * @brief Validate PractitionerRole resource (virtual method)
 * @param self PractitionerRole to validate
 * @return true if valid, false otherwise
 */
bool fhir_practitionerrole_validate(const FHIRPractitionerRole* self);

/* ========================================================================== */
/* PractitionerRole-Specific Methods                                          */
/* ========================================================================== */

/**
 * @brief Check if PractitionerRole is active (virtual method)
 * @param self PractitionerRole to check
 * @return true if active, false otherwise
 */
bool fhir_practitionerrole_is_active(const FHIRPractitionerRole* self);

/**
 * @brief Get PractitionerRole display name (virtual method)
 * @param self PractitionerRole to get name from
 * @return Display name or NULL
 */
const char* fhir_practitionerrole_get_display_name(const FHIRPractitionerRole* self);

/**
 * @brief Register PractitionerRole resource type
 * @return true on success, false on failure
 */
bool fhir_practitionerrole_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_PRACTITIONERROLE_H */