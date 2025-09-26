/**
 * @file fhir_practitioner.h
 * @brief FHIR R5 Practitioner resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#ifndef FHIR_PRACTITIONER_H
#define FHIR_PRACTITIONER_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Practitioner-Specific Enumerations                                        */
/* ========================================================================== */

/**
 * @brief Practitioner gender enumeration (same as Patient)
 */
typedef enum {
    FHIR_PRACTITIONER_GENDER_UNKNOWN = 0,
    FHIR_PRACTITIONER_GENDER_MALE,
    FHIR_PRACTITIONER_GENDER_FEMALE,
    FHIR_PRACTITIONER_GENDER_OTHER
} FHIRPractitionerGender;

/* ========================================================================== */
/* Practitioner Sub-structures                                               */
/* ========================================================================== */

/**
 * @brief Practitioner qualification information
 */
typedef struct FHIRPractitionerQualification {
    FHIRElement base;
    FHIRIdentifier** identifier;
    size_t identifier_count;
    FHIRCodeableConcept* code;
    FHIRPeriod* period;
    FHIRReference* issuer;
} FHIRPractitionerQualification;

/**
 * @brief Practitioner communication languages
 */
typedef struct FHIRPractitionerCommunication {
    FHIRElement base;
    FHIRCodeableConcept* language;
    FHIRBoolean* preferred;
} FHIRPractitionerCommunication;

/* ========================================================================== */
/* Practitioner Resource Structure                                           */
/* ========================================================================== */

/**
 * @brief FHIR R5 Practitioner resource structure
 * 
 * A person who is directly or indirectly involved in the provisioning of healthcare.
 */
FHIR_RESOURCE_DEFINE(Practitioner)
    // Practitioner-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRBoolean* active;
    
    FHIRHumanName** name;
    size_t name_count;
    
    FHIRContactPoint** telecom;
    size_t telecom_count;
    
    FHIRPractitionerGender gender;
    
    FHIRDate* birth_date;
    
    // Deceased information (choice type)
    FHIRBoolean* deceased_boolean;
    FHIRDateTime* deceased_date_time;
    
    FHIRAddress** address;
    size_t address_count;
    
    FHIRAttachment** photo;
    size_t photo_count;
    
    FHIRPractitionerQualification** qualification;
    size_t qualification_count;
    
    FHIRPractitionerCommunication** communication;
    size_t communication_count;
};

/* ========================================================================== */
/* Practitioner Factory and Lifecycle Methods                               */
/* ========================================================================== */

/**
 * @brief Create a new Practitioner resource
 * @param id Resource identifier (required)
 * @return Pointer to new Practitioner or NULL on failure
 */
FHIRPractitioner* fhir_practitioner_create(const char* id);

/**
 * @brief Destroy Practitioner resource (virtual destructor)
 * @param self Practitioner to destroy
 */
void fhir_practitioner_destroy(FHIRPractitioner* self);

/**
 * @brief Clone Practitioner resource (virtual clone)
 * @param self Practitioner to clone
 * @return Cloned Practitioner or NULL on failure
 */
FHIRPractitioner* fhir_practitioner_clone(const FHIRPractitioner* self);

/* ========================================================================== */
/* Practitioner Serialization Methods                                        */
/* ========================================================================== */

/**
 * @brief Convert Practitioner to JSON (virtual method)
 * @param self Practitioner to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_practitioner_to_json(const FHIRPractitioner* self);

/**
 * @brief Load Practitioner from JSON (virtual method)
 * @param self Practitioner to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_practitioner_from_json(FHIRPractitioner* self, const cJSON* json);

/**
 * @brief Parse Practitioner from JSON string
 * @param json_string JSON string
 * @return New Practitioner or NULL on failure
 */
FHIRPractitioner* fhir_practitioner_parse(const char* json_string);

/* ========================================================================== */
/* Practitioner Validation Methods                                           */
/* ========================================================================== */

/**
 * @brief Validate Practitioner resource (virtual method)
 * @param self Practitioner to validate
 * @return true if valid, false otherwise
 */
bool fhir_practitioner_validate(const FHIRPractitioner* self);

/* ========================================================================== */
/* Practitioner-Specific Methods                                             */
/* ========================================================================== */

/**
 * @brief Check if Practitioner is active (virtual method)
 * @param self Practitioner to check
 * @return true if active, false otherwise
 */
bool fhir_practitioner_is_active(const FHIRPractitioner* self);

/**
 * @brief Get Practitioner display name (virtual method)
 * @param self Practitioner to get name from
 * @return Display name or NULL
 */
const char* fhir_practitioner_get_display_name(const FHIRPractitioner* self);

/**
 * @brief Check if Practitioner is deceased
 * @param self Practitioner to check
 * @return true if deceased, false otherwise
 */
bool fhir_practitioner_is_deceased(const FHIRPractitioner* self);

/**
 * @brief Add qualification to Practitioner
 * @param self Practitioner to modify
 * @param qualification Qualification to add
 * @return true on success, false on failure
 */
bool fhir_practitioner_add_qualification(FHIRPractitioner* self, 
                                        const FHIRPractitionerQualification* qualification);

/**
 * @brief Get qualifications by code
 * @param self Practitioner to search
 * @param code Qualification code to search for
 * @param count Output parameter for result count
 * @return Array of matching qualifications or NULL
 */
FHIRPractitionerQualification** fhir_practitioner_get_qualifications_by_code(
    const FHIRPractitioner* self, const char* code, size_t* count);

/**
 * @brief Register Practitioner resource type
 * @return true on success, false on failure
 */
bool fhir_practitioner_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_PRACTITIONER_H */