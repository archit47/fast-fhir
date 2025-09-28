/**
 * @file fhir_patient.h
 * @brief FHIR R5 Patient resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * This header defines the C interface for the FHIR R5 Patient resource
 * using Object-Oriented Programming principles in C.
 */

#ifndef FHIR_PATIENT_H
#define FHIR_PATIENT_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Patient-Specific Enumerations                                             */
/* ========================================================================== */

/**
 * @brief Patient gender enumeration
 */
typedef enum {
    FHIR_PATIENT_GENDER_UNKNOWN = 0,
    FHIR_PATIENT_GENDER_MALE,
    FHIR_PATIENT_GENDER_FEMALE,
    FHIR_PATIENT_GENDER_OTHER
} FHIRPatientGender;

/**
 * @brief Patient link type enumeration
 */
typedef enum {
    FHIR_PATIENT_LINK_TYPE_REPLACED_BY,
    FHIR_PATIENT_LINK_TYPE_REPLACES,
    FHIR_PATIENT_LINK_TYPE_REFER,
    FHIR_PATIENT_LINK_TYPE_SEEALSO
} FHIRPatientLinkType;

/* ========================================================================== */
/* Patient Sub-structures                                                    */
/* ========================================================================== */

/**
 * @brief Patient contact information
 */
typedef struct FHIRPatientContact {
    FHIRElement base;
    FHIRCodeableConcept** relationship;
    size_t relationship_count;
    FHIRHumanName* name;
    FHIRContactPoint** telecom;
    size_t telecom_count;
    FHIRAddress* address;
    FHIRPatientGender gender;
    FHIRReference* organization;
    FHIRPeriod* period;
} FHIRPatientContact;

/**
 * @brief Patient communication preferences
 */
typedef struct FHIRPatientCommunication {
    FHIRElement base;
    FHIRCodeableConcept* language;
    FHIRBoolean* preferred;
} FHIRPatientCommunication;

/**
 * @brief Patient link to another patient resource
 */
typedef struct FHIRPatientLink {
    FHIRElement base;
    FHIRReference* other;
    FHIRPatientLinkType type;
} FHIRPatientLink;

/* ========================================================================== */
/* Patient Resource Structure                                                */
/* ========================================================================== */

/**
 * @brief FHIR R5 Patient resource structure
 * 
 * Demographics and other administrative information about an individual
 * or animal receiving care or other health-related services.
 */
FHIR_RESOURCE_DEFINE(Patient)
    // Patient-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRBoolean* active;
    
    FHIRHumanName** name;
    size_t name_count;
    
    FHIRContactPoint** telecom;
    size_t telecom_count;
    
    FHIRPatientGender gender;
    
    FHIRDate* birth_date;
    
    // Deceased information (choice type)
    FHIRBoolean* deceased_boolean;
    FHIRDateTime* deceased_date_time;
    
    FHIRAddress** address;
    size_t address_count;
    
    FHIRCodeableConcept* marital_status;
    
    // Multiple birth information (choice type)
    FHIRBoolean* multiple_birth_boolean;
    FHIRInteger* multiple_birth_integer;
    
    FHIRAttachment** photo;
    size_t photo_count;
    
    FHIRPatientContact** contact;
    size_t contact_count;
    
    FHIRPatientCommunication** communication;
    size_t communication_count;
    
    FHIRReference** general_practitioner;
    size_t general_practitioner_count;
    
    FHIRReference* managing_organization;
    
    FHIRPatientLink** link;
    size_t link_count;
};

/* ========================================================================== */
/* Patient Factory and Lifecycle Methods                                     */
/* ========================================================================== */

/**
 * @brief Create a new Patient resource
 * @param id Resource identifier (required)
 * @return Pointer to new Patient or NULL on failure
 */
FHIRPatient* fhir_patient_create(const char* id);

/**
 * @brief Destroy Patient resource (virtual destructor)
 * @param self Patient to destroy
 */
void fhir_patient_destroy(FHIRPatient* self);

/**
 * @brief Clone Patient resource (virtual clone)
 * @param self Patient to clone
 * @return Cloned Patient or NULL on failure
 */
FHIRPatient* fhir_patient_clone(const FHIRPatient* self);/* =====
===================================================================== */
/* Patient Serialization Methods                                             */
/* ========================================================================== */

/**
 * @brief Convert Patient to JSON (virtual method)
 * @param self Patient to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_patient_to_json(const FHIRPatient* self);

/**
 * @brief Load Patient from JSON (virtual method)
 * @param self Patient to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_patient_from_json(FHIRPatient* self, const cJSON* json);

/**
 * @brief Parse Patient from JSON string
 * @param json_string JSON string
 * @return New Patient or NULL on failure
 */
FHIRPatient* fhir_patient_parse(const char* json_string);

/* ========================================================================== */
/* Patient Validation Methods                                                */
/* ========================================================================== */

/**
 * @brief Validate Patient resource (virtual method)
 * @param self Patient to validate
 * @return true if valid, false otherwise
 */
bool fhir_patient_validate(const FHIRPatient* self);

/**
 * @brief Get validation errors for Patient
 * @param self Patient to validate
 * @param count Output parameter for error count
 * @return Array of error strings (must be freed by caller)
 */
char** fhir_patient_get_validation_errors(const FHIRPatient* self, size_t* count);

/* ========================================================================== */
/* Patient Comparison Methods                                                */
/* ========================================================================== */

/**
 * @brief Check if two Patients are equal (virtual method)
 * @param self First Patient
 * @param other Second Patient
 * @return true if equal, false otherwise
 */
bool fhir_patient_equals(const FHIRPatient* self, const FHIRPatient* other);

/**
 * @brief Compare two Patients (virtual method)
 * @param self First Patient
 * @param other Second Patient
 * @return -1, 0, or 1 for less than, equal, or greater than
 */
int fhir_patient_compare(const FHIRPatient* self, const FHIRPatient* other);

/* ========================================================================== */
/* Patient String Representation                                             */
/* ========================================================================== */

/**
 * @brief Convert Patient to string representation (virtual method)
 * @param self Patient to convert
 * @return String representation (must be freed by caller)
 */
char* fhir_patient_to_string(const FHIRPatient* self);

/* ========================================================================== */
/* Patient-Specific Methods                                                  */
/* ========================================================================== */

/**
 * @brief Check if Patient is active (virtual method)
 * @param self Patient to check
 * @return true if active, false otherwise
 */
bool fhir_patient_is_active(const FHIRPatient* self);

/**
 * @brief Get Patient display name (virtual method)
 * @param self Patient to get name from
 * @return Display name or NULL
 */
const char* fhir_patient_get_display_name(const FHIRPatient* self);

/**
 * @brief Check if Patient is deceased
 * @param self Patient to check
 * @return true if deceased, false otherwise
 */
bool fhir_patient_is_deceased(const FHIRPatient* self);

/**
 * @brief Get Patient age in years
 * @param self Patient to calculate age for
 * @return Age in years or -1 if birth date not available
 */
int fhir_patient_get_age(const FHIRPatient* self);

/**
 * @brief Get Patient's primary name
 * @param self Patient to get name from
 * @return Primary name or NULL
 */
const FHIRHumanName* fhir_patient_get_primary_name(const FHIRPatient* self);

/**
 * @brief Get Patient's primary address
 * @param self Patient to get address from
 * @return Primary address or NULL
 */
const FHIRAddress* fhir_patient_get_primary_address(const FHIRPatient* self);

/* ========================================================================== */
/* Patient Modification Methods                                              */
/* ========================================================================== */

/**
 * @brief Set Patient active status
 * @param self Patient to modify
 * @param active Active status
 * @return true on success, false on failure
 */
bool fhir_patient_set_active(FHIRPatient* self, bool active);

/**
 * @brief Set Patient gender
 * @param self Patient to modify
 * @param gender Gender value
 * @return true on success, false on failure
 */
bool fhir_patient_set_gender(FHIRPatient* self, FHIRPatientGender gender);

/**
 * @brief Set Patient birth date
 * @param self Patient to modify
 * @param birth_date Birth date string (YYYY-MM-DD format)
 * @return true on success, false on failure
 */
bool fhir_patient_set_birth_date(FHIRPatient* self, const char* birth_date);

/**
 * @brief Add identifier to Patient
 * @param self Patient to modify
 * @param identifier Identifier to add
 * @return true on success, false on failure
 */
bool fhir_patient_add_identifier(FHIRPatient* self, const FHIRIdentifier* identifier);

/**
 * @brief Add name to Patient
 * @param self Patient to modify
 * @param name Name to add
 * @return true on success, false on failure
 */
bool fhir_patient_add_name(FHIRPatient* self, const FHIRHumanName* name);

/**
 * @brief Add address to Patient
 * @param self Patient to modify
 * @param address Address to add
 * @return true on success, false on failure
 */
bool fhir_patient_add_address(FHIRPatient* self, const FHIRAddress* address);

/**
 * @brief Add telecom to Patient
 * @param self Patient to modify
 * @param telecom Telecom to add
 * @return true on success, false on failure
 */
bool fhir_patient_add_telecom(FHIRPatient* self, const FHIRContactPoint* telecom);

/* ========================================================================== */
/* Patient Utility Functions                                                 */
/* ========================================================================== */

/**
 * @brief Convert gender enum to string
 * @param gender Gender enum
 * @return String representation or NULL for unknown gender
 */
const char* fhir_patient_gender_to_string(FHIRPatientGender gender);

/**
 * @brief Convert string to gender enum
 * @param gender_str String representation
 * @return Gender enum or FHIR_PATIENT_GENDER_UNKNOWN for invalid string
 */
FHIRPatientGender fhir_patient_gender_from_string(const char* gender_str);

/**
 * @brief Register Patient resource type with the resource system
 * @return true on success, false on failure
 */
bool fhir_patient_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_PATIENT_H */