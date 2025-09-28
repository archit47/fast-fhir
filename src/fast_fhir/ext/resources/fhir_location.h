/**
 * @file fhir_location.h
 * @brief FHIR R5 Location resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * Details and position information for a physical place
 */

#ifndef FHIR_LOCATION_H
#define FHIR_LOCATION_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Location status enumeration
 */
typedef enum {
    FHIRLOCATIONSTATUS_ACTIVE = 0,
    FHIRLOCATIONSTATUS_SUSPENDED = 1,
    FHIRLOCATIONSTATUS_INACTIVE = 2,
} FHIRLocationStatus;

/**
 * @brief Location mode enumeration
 */
typedef enum {
    FHIRLOCATIONMODE_INSTANCE = 0,
    FHIRLOCATIONMODE_KIND = 1,
} FHIRLocationMode;

/**
 * @brief FHIR R5 Location resource structure
 * 
 * Details and position information for a physical place
 */
FHIR_RESOURCE_DEFINE(Location)
    // Location-specific fields
    FHIRLocationStatus status;
    
    FHIRCoding* operational_status;
    
    FHIRString* name;
    
    FHIRString** alias;
    size_t alias_count;
    
    FHIRMarkdown* description;
    
    FHIRLocationMode mode;
    
    FHIRCodeableConcept** type;
    size_t type_count;
    
    FHIRExtendedContactDetail** contact;
    size_t contact_count;
    
    FHIRAddress* address;
    
    FHIRCodeableConcept* physical_type;
    
    FHIRLocationPosition* position;
    
    FHIRReference* managing_organization;
    
    FHIRReference* part_of;
    
    FHIRCodeableConcept** characteristic;
    size_t characteristic_count;
    
    FHIRAvailability** hours_of_operation;
    size_t hours_of_operation_count;
    
    FHIRVirtualServiceDetail** virtual_service;
    size_t virtual_service_count;
    
};

/* ========================================================================== */
/* Location Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new Location resource
 * @param id Resource identifier (required)
 * @return Pointer to new Location or NULL on failure
 */
FHIRLocation* fhir_location_create(const char* id);

/**
 * @brief Destroy Location resource (virtual destructor)
 * @param self Location to destroy
 */
void fhir_location_destroy(FHIRLocation* self);

/**
 * @brief Clone Location resource (virtual clone)
 * @param self Location to clone
 * @return Cloned Location or NULL on failure
 */
FHIRLocation* fhir_location_clone(const FHIRLocation* self);

/* ========================================================================== */
/* Location Serialization Methods                                     */
/* ========================================================================== */

/**
 * @brief Convert Location to JSON (virtual method)
 * @param self Location to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_location_to_json(const FHIRLocation* self);

/**
 * @brief Load Location from JSON (virtual method)
 * @param self Location to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_location_from_json(FHIRLocation* self, const cJSON* json);

/**
 * @brief Parse Location from JSON string
 * @param json_string JSON string
 * @return New Location or NULL on failure
 */
FHIRLocation* fhir_location_parse(const char* json_string);

/* ========================================================================== */
/* Location Validation Methods                                        */
/* ========================================================================== */

/**
 * @brief Validate Location resource (virtual method)
 * @param self Location to validate
 * @return true if valid, false otherwise
 */
bool fhir_location_validate(const FHIRLocation* self);

/* ========================================================================== */
/* Location-Specific Methods                                          */
/* ========================================================================== */

/**
 * @brief Check if Location is active (virtual method)
 * @param self Location to check
 * @return true if active, false otherwise
 */
bool fhir_location_is_active(const FHIRLocation* self);

/**
 * @brief Get Location display name (virtual method)
 * @param self Location to get name from
 * @return Display name or NULL
 */
const char* fhir_location_get_display_name(const FHIRLocation* self);

/**
 * @brief Register Location resource type
 * @return true on success, false on failure
 */
bool fhir_location_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_LOCATION_H */