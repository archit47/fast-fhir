/**
 * @file fhir_visionprescription.h
 * @brief FHIR R5 VisionPrescription resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * An authorization for the provision of glasses and/or contact lenses to a patient
 */

#ifndef FHIR_VISIONPRESCRIPTION_H
#define FHIR_VISIONPRESCRIPTION_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* VisionPrescription-Specific Enumerations                                  */
/* ========================================================================== */

/**
 * @brief VisionPrescription status enumeration
 */
typedef enum {
    FHIR_VISIONPRESCRIPTION_STATUS_ACTIVE = 0,
    FHIR_VISIONPRESCRIPTION_STATUS_CANCELLED,
    FHIR_VISIONPRESCRIPTION_STATUS_DRAFT,
    FHIR_VISIONPRESCRIPTION_STATUS_ENTERED_IN_ERROR
} FHIRVisionPrescriptionStatus;

/**
 * @brief Vision eye enumeration
 */
typedef enum {
    FHIR_VISION_EYE_RIGHT = 0,
    FHIR_VISION_EYE_LEFT
} FHIRVisionEye;

/**
 * @brief Vision base enumeration
 */
typedef enum {
    FHIR_VISION_BASE_UP = 0,
    FHIR_VISION_BASE_DOWN,
    FHIR_VISION_BASE_IN,
    FHIR_VISION_BASE_OUT
} FHIRVisionBase;

/* ========================================================================== */
/* VisionPrescription Sub-structures                                         */
/* ========================================================================== */

/**
 * @brief VisionPrescription lens specification information
 */
typedef struct FHIRVisionPrescriptionLensSpecification {
    FHIRElement base;
    FHIRCodeableConcept* product;
    FHIRVisionEye eye;
    FHIRDecimal* sphere;
    FHIRDecimal* cylinder;
    FHIRInteger* axis;
    FHIRQuantity** prism;
    size_t prism_count;
    FHIRDecimal* add;
    FHIRDecimal* power;
    FHIRDecimal* back_curve;
    FHIRDecimal* diameter;
    FHIRQuantity* duration;
    FHIRString* color;
    FHIRString* brand;
    FHIRAnnotation** note;
    size_t note_count;
} FHIRVisionPrescriptionLensSpecification;

/**
 * @brief VisionPrescription prism information
 */
typedef struct FHIRVisionPrescriptionPrism {
    FHIRElement base;
    FHIRDecimal* amount;
    FHIRVisionBase base_direction;
} FHIRVisionPrescriptionPrism;

/* ========================================================================== */
/* VisionPrescription Resource Structure                                     */
/* ========================================================================== */

/**
 * @brief FHIR R5 VisionPrescription resource structure
 * 
 * An authorization for the provision of glasses and/or contact lenses
 */
FHIR_RESOURCE_DEFINE(VisionPrescription)
    // VisionPrescription-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRVisionPrescriptionStatus status;
    
    FHIRDateTime* created;
    
    FHIRReference* patient;
    
    FHIRReference* encounter;
    
    FHIRDateTime* date_written;
    
    FHIRReference* prescriber;
    
    FHIRVisionPrescriptionLensSpecification** lens_specification;
    size_t lens_specification_count;
};

/* ========================================================================== */
/* VisionPrescription Factory and Lifecycle Methods                         */
/* ========================================================================== */

/**
 * @brief Create a new VisionPrescription resource
 * @param id Resource identifier (required)
 * @return Pointer to new VisionPrescription or NULL on failure
 */
FHIRVisionPrescription* fhir_visionprescription_create(const char* id);

/**
 * @brief Destroy VisionPrescription resource (virtual destructor)
 * @param self VisionPrescription to destroy
 */
void fhir_visionprescription_destroy(FHIRVisionPrescription* self);

/**
 * @brief Clone VisionPrescription resource (virtual clone)
 * @param self VisionPrescription to clone
 * @return Cloned VisionPrescription or NULL on failure
 */
FHIRVisionPrescription* fhir_visionprescription_clone(const FHIRVisionPrescription* self);

/* ========================================================================== */
/* VisionPrescription Serialization Methods                                  */
/* ========================================================================== */

/**
 * @brief Convert VisionPrescription to JSON (virtual method)
 * @param self VisionPrescription to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_visionprescription_to_json(const FHIRVisionPrescription* self);

/**
 * @brief Load VisionPrescription from JSON (virtual method)
 * @param self VisionPrescription to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_visionprescription_from_json(FHIRVisionPrescription* self, const cJSON* json);

/**
 * @brief Parse VisionPrescription from JSON string
 * @param json_string JSON string
 * @return New VisionPrescription or NULL on failure
 */
FHIRVisionPrescription* fhir_visionprescription_parse(const char* json_string);

/* ========================================================================== */
/* VisionPrescription Validation Methods                                     */
/* ========================================================================== */

/**
 * @brief Validate VisionPrescription resource (virtual method)
 * @param self VisionPrescription to validate
 * @return true if valid, false otherwise
 */
bool fhir_visionprescription_validate(const FHIRVisionPrescription* self);

/* ========================================================================== */
/* VisionPrescription-Specific Methods                                       */
/* ========================================================================== */

/**
 * @brief Check if VisionPrescription is active (virtual method)
 * @param self VisionPrescription to check
 * @return true if status is active, false otherwise
 */
bool fhir_visionprescription_is_active(const FHIRVisionPrescription* self);

/**
 * @brief Get VisionPrescription display name (virtual method)
 * @param self VisionPrescription to get name from
 * @return Display name or NULL
 */
const char* fhir_visionprescription_get_display_name(const FHIRVisionPrescription* self);

/**
 * @brief Set VisionPrescription status
 * @param self VisionPrescription to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_visionprescription_set_status(FHIRVisionPrescription* self, FHIRVisionPrescriptionStatus status);

/**
 * @brief Add lens specification to VisionPrescription
 * @param self VisionPrescription to modify
 * @param lens_spec Lens specification to add
 * @return true on success, false on failure
 */
bool fhir_visionprescription_add_lens_specification(FHIRVisionPrescription* self, 
                                                   const FHIRVisionPrescriptionLensSpecification* lens_spec);

/**
 * @brief Get lens specification for specific eye
 * @param self VisionPrescription to search
 * @param eye Eye to search for
 * @return Lens specification for the eye or NULL
 */
FHIRVisionPrescriptionLensSpecification* fhir_visionprescription_get_lens_for_eye(
    const FHIRVisionPrescription* self, FHIRVisionEye eye);

/**
 * @brief Check if prescription is for glasses
 * @param self VisionPrescription to check
 * @return true if any lens specification is for glasses, false otherwise
 */
bool fhir_visionprescription_is_for_glasses(const FHIRVisionPrescription* self);

/**
 * @brief Check if prescription is for contact lenses
 * @param self VisionPrescription to check
 * @return true if any lens specification is for contacts, false otherwise
 */
bool fhir_visionprescription_is_for_contacts(const FHIRVisionPrescription* self);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_visionprescription_status_to_string(FHIRVisionPrescriptionStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_VISIONPRESCRIPTION_STATUS_DRAFT for invalid string
 */
FHIRVisionPrescriptionStatus fhir_visionprescription_status_from_string(const char* status_str);

/**
 * @brief Convert eye enum to string
 * @param eye Eye enum
 * @return String representation or NULL for unknown eye
 */
const char* fhir_vision_eye_to_string(FHIRVisionEye eye);

/**
 * @brief Convert string to eye enum
 * @param eye_str String representation
 * @return Eye enum or FHIR_VISION_EYE_RIGHT for invalid string
 */
FHIRVisionEye fhir_vision_eye_from_string(const char* eye_str);

/**
 * @brief Convert base enum to string
 * @param base Base enum
 * @return String representation or NULL for unknown base
 */
const char* fhir_vision_base_to_string(FHIRVisionBase base);

/**
 * @brief Convert string to base enum
 * @param base_str String representation
 * @return Base enum or FHIR_VISION_BASE_UP for invalid string
 */
FHIRVisionBase fhir_vision_base_from_string(const char* base_str);

/**
 * @brief Register VisionPrescription resource type
 * @return true on success, false on failure
 */
bool fhir_visionprescription_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_VISIONPRESCRIPTION_H */