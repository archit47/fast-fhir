/**
 * @file fhir_observation.h
 * @brief FHIR R5 Observation resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * Measurements and simple assertions made about a patient, device or other subject
 */

#ifndef FHIR_OBSERVATION_H
#define FHIR_OBSERVATION_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Observation-Specific Enumerations                                         */
/* ========================================================================== */

/**
 * @brief Observation status enumeration
 */
typedef enum {
    FHIR_OBSERVATION_STATUS_REGISTERED = 0,
    FHIR_OBSERVATION_STATUS_PRELIMINARY,
    FHIR_OBSERVATION_STATUS_FINAL,
    FHIR_OBSERVATION_STATUS_AMENDED,
    FHIR_OBSERVATION_STATUS_CORRECTED,
    FHIR_OBSERVATION_STATUS_CANCELLED,
    FHIR_OBSERVATION_STATUS_ENTERED_IN_ERROR,
    FHIR_OBSERVATION_STATUS_UNKNOWN
} FHIRObservationStatus;

/* ========================================================================== */
/* Observation Sub-structures                                                */
/* ========================================================================== */

/**
 * @brief Observation component information
 */
typedef struct FHIRObservationComponent {
    FHIRElement base;
    FHIRCodeableConcept* code;
    
    // Value (choice type)
    FHIRQuantity* value_quantity;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRBoolean* value_boolean;
    FHIRInteger* value_integer;
    FHIRRange* value_range;
    FHIRRatio* value_ratio;
    FHIRSampledData* value_sampled_data;
    FHIRTime* value_time;
    FHIRDateTime* value_date_time;
    FHIRPeriod* value_period;
    FHIRAttachment* value_attachment;
    FHIRReference* value_reference;
    
    FHIRCodeableConcept* data_absent_reason;
    FHIRCodeableConcept** interpretation;
    size_t interpretation_count;
    FHIRObservationReferenceRange** reference_range;
    size_t reference_range_count;
} FHIRObservationComponent;

/**
 * @brief Observation reference range information
 */
typedef struct FHIRObservationReferenceRange {
    FHIRElement base;
    FHIRQuantity* low;
    FHIRQuantity* high;
    FHIRCodeableConcept* normal_value;
    FHIRCodeableConcept* type;
    FHIRCodeableConcept** applies_to;
    size_t applies_to_count;
    FHIRRange* age;
    FHIRString* text;
} FHIRObservationReferenceRange;

/* ========================================================================== */
/* Observation Resource Structure                                            */
/* ========================================================================== */

/**
 * @brief FHIR R5 Observation resource structure
 * 
 * Measurements and simple assertions made about a patient, device or other subject
 */
FHIR_RESOURCE_DEFINE(Observation)
    // Observation-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRReference** instantiates_canonical;
    size_t instantiates_canonical_count;
    
    FHIRReference** instantiates_reference;
    size_t instantiates_reference_count;
    
    FHIRReference** based_on;
    size_t based_on_count;
    
    FHIRReference** triggered_by;
    size_t triggered_by_count;
    
    FHIRReference** part_of;
    size_t part_of_count;
    
    FHIRObservationStatus status;
    
    FHIRCodeableConcept** category;
    size_t category_count;
    
    FHIRCodeableConcept* code;
    
    FHIRReference* subject;
    
    FHIRReference** focus;
    size_t focus_count;
    
    FHIRReference* encounter;
    
    // Effective (choice type)
    FHIRDateTime* effective_date_time;
    FHIRPeriod* effective_period;
    FHIRTiming* effective_timing;
    FHIRInstant* effective_instant;
    
    FHIRInstant* issued;
    
    FHIRReference** performer;
    size_t performer_count;
    
    // Value (choice type)
    FHIRQuantity* value_quantity;
    FHIRCodeableConcept* value_codeable_concept;
    FHIRString* value_string;
    FHIRBoolean* value_boolean;
    FHIRInteger* value_integer;
    FHIRRange* value_range;
    FHIRRatio* value_ratio;
    FHIRSampledData* value_sampled_data;
    FHIRTime* value_time;
    FHIRDateTime* value_date_time;
    FHIRPeriod* value_period;
    FHIRAttachment* value_attachment;
    FHIRReference* value_reference;
    
    FHIRCodeableConcept* data_absent_reason;
    
    FHIRCodeableConcept** interpretation;
    size_t interpretation_count;
    
    FHIRAnnotation** note;
    size_t note_count;
    
    FHIRCodeableConcept* body_site;
    
    FHIRCodeableConcept* method;
    
    FHIRReference* specimen;
    
    FHIRReference* device;
    
    FHIRObservationReferenceRange** reference_range;
    size_t reference_range_count;
    
    FHIRReference** has_member;
    size_t has_member_count;
    
    FHIRReference** derived_from;
    size_t derived_from_count;
    
    FHIRObservationComponent** component;
    size_t component_count;
};

/* ========================================================================== */
/* Observation Factory and Lifecycle Methods                                 */
/* ========================================================================== */

/**
 * @brief Create a new Observation resource
 * @param id Resource identifier (required)
 * @return Pointer to new Observation or NULL on failure
 */
FHIRObservation* fhir_observation_create(const char* id);

/**
 * @brief Destroy Observation resource (virtual destructor)
 * @param self Observation to destroy
 */
void fhir_observation_destroy(FHIRObservation* self);

/**
 * @brief Clone Observation resource (virtual clone)
 * @param self Observation to clone
 * @return Cloned Observation or NULL on failure
 */
FHIRObservation* fhir_observation_clone(const FHIRObservation* self);

/* ========================================================================== */
/* Observation Serialization Methods                                         */
/* ========================================================================== */

/**
 * @brief Convert Observation to JSON (virtual method)
 * @param self Observation to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_observation_to_json(const FHIRObservation* self);

/**
 * @brief Load Observation from JSON (virtual method)
 * @param self Observation to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_observation_from_json(FHIRObservation* self, const cJSON* json);

/**
 * @brief Parse Observation from JSON string
 * @param json_string JSON string
 * @return New Observation or NULL on failure
 */
FHIRObservation* fhir_observation_parse(const char* json_string);

/* ========================================================================== */
/* Observation Validation Methods                                            */
/* ========================================================================== */

/**
 * @brief Validate Observation resource (virtual method)
 * @param self Observation to validate
 * @return true if valid, false otherwise
 */
bool fhir_observation_validate(const FHIRObservation* self);

/* ========================================================================== */
/* Observation-Specific Methods                                              */
/* ========================================================================== */

/**
 * @brief Check if Observation is active (virtual method)
 * @param self Observation to check
 * @return true if status is final or amended, false otherwise
 */
bool fhir_observation_is_active(const FHIRObservation* self);

/**
 * @brief Get Observation display name (virtual method)
 * @param self Observation to get name from
 * @return Display name or NULL
 */
const char* fhir_observation_get_display_name(const FHIRObservation* self);

/**
 * @brief Check if Observation has a value
 * @param self Observation to check
 * @return true if any value is present, false otherwise
 */
bool fhir_observation_has_value(const FHIRObservation* self);

/**
 * @brief Get Observation value as string
 * @param self Observation to get value from
 * @return String representation of value or NULL
 */
char* fhir_observation_get_value_string(const FHIRObservation* self);

/**
 * @brief Set Observation status
 * @param self Observation to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_observation_set_status(FHIRObservation* self, FHIRObservationStatus status);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_observation_status_to_string(FHIRObservationStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_OBSERVATION_STATUS_UNKNOWN for invalid string
 */
FHIRObservationStatus fhir_observation_status_from_string(const char* status_str);

/**
 * @brief Register Observation resource type
 * @return true on success, false on failure
 */
bool fhir_observation_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_OBSERVATION_H */