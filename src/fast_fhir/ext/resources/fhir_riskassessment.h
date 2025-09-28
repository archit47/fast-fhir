/**
 * @file fhir_riskassessment.h
 * @brief FHIR R5 RiskAssessment resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 * 
 * An assessment of the likely outcome(s) for a patient or other subject as well as the likelihood of each outcome
 */

#ifndef FHIR_RISKASSESSMENT_H
#define FHIR_RISKASSESSMENT_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* RiskAssessment-Specific Enumerations                                      */
/* ========================================================================== */

/**
 * @brief RiskAssessment status enumeration
 */
typedef enum {
    FHIR_RISKASSESSMENT_STATUS_REGISTERED = 0,
    FHIR_RISKASSESSMENT_STATUS_PRELIMINARY,
    FHIR_RISKASSESSMENT_STATUS_FINAL,
    FHIR_RISKASSESSMENT_STATUS_AMENDED,
    FHIR_RISKASSESSMENT_STATUS_CORRECTED,
    FHIR_RISKASSESSMENT_STATUS_CANCELLED,
    FHIR_RISKASSESSMENT_STATUS_ENTERED_IN_ERROR,
    FHIR_RISKASSESSMENT_STATUS_UNKNOWN
} FHIRRiskAssessmentStatus;

/* ========================================================================== */
/* RiskAssessment Sub-structures                                             */
/* ========================================================================== */

/**
 * @brief RiskAssessment prediction information
 */
typedef struct FHIRRiskAssessmentPrediction {
    FHIRElement base;
    FHIRCodeableConcept* outcome;
    
    // Probability (choice type)
    FHIRDecimal* probability_decimal;
    FHIRRange* probability_range;
    
    FHIRCodeableConcept* qualitative_risk;
    FHIRDecimal* relative_risk;
    
    // When (choice type)
    FHIRPeriod* when_period;
    FHIRRange* when_range;
    
    FHIRString* rationale;
} FHIRRiskAssessmentPrediction;

/* ========================================================================== */
/* RiskAssessment Resource Structure                                         */
/* ========================================================================== */

/**
 * @brief FHIR R5 RiskAssessment resource structure
 * 
 * An assessment of the likely outcome(s) for a patient or other subject
 */
FHIR_RESOURCE_DEFINE(RiskAssessment)
    // RiskAssessment-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRReference* based_on;
    
    FHIRReference* parent;
    
    FHIRRiskAssessmentStatus status;
    
    FHIRCodeableConcept* method;
    
    FHIRCodeableConcept* code;
    
    FHIRReference* subject;
    
    FHIRReference* encounter;
    
    // Occurrence (choice type)
    FHIRDateTime* occurrence_date_time;
    FHIRPeriod* occurrence_period;
    
    FHIRReference* condition;
    
    FHIRReference* performer;
    
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    
    FHIRReference** basis;
    size_t basis_count;
    
    FHIRRiskAssessmentPrediction** prediction;
    size_t prediction_count;
    
    FHIRString* mitigation;
    
    FHIRAnnotation** note;
    size_t note_count;
};

/* ========================================================================== */
/* RiskAssessment Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new RiskAssessment resource
 * @param id Resource identifier (required)
 * @return Pointer to new RiskAssessment or NULL on failure
 */
FHIRRiskAssessment* fhir_riskassessment_create(const char* id);

/**
 * @brief Destroy RiskAssessment resource (virtual destructor)
 * @param self RiskAssessment to destroy
 */
void fhir_riskassessment_destroy(FHIRRiskAssessment* self);

/**
 * @brief Clone RiskAssessment resource (virtual clone)
 * @param self RiskAssessment to clone
 * @return Cloned RiskAssessment or NULL on failure
 */
FHIRRiskAssessment* fhir_riskassessment_clone(const FHIRRiskAssessment* self);

/* ========================================================================== */
/* RiskAssessment Serialization Methods                                      */
/* ========================================================================== */

/**
 * @brief Convert RiskAssessment to JSON (virtual method)
 * @param self RiskAssessment to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_riskassessment_to_json(const FHIRRiskAssessment* self);

/**
 * @brief Load RiskAssessment from JSON (virtual method)
 * @param self RiskAssessment to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_riskassessment_from_json(FHIRRiskAssessment* self, const cJSON* json);

/**
 * @brief Parse RiskAssessment from JSON string
 * @param json_string JSON string
 * @return New RiskAssessment or NULL on failure
 */
FHIRRiskAssessment* fhir_riskassessment_parse(const char* json_string);

/* ========================================================================== */
/* RiskAssessment Validation Methods                                         */
/* ========================================================================== */

/**
 * @brief Validate RiskAssessment resource (virtual method)
 * @param self RiskAssessment to validate
 * @return true if valid, false otherwise
 */
bool fhir_riskassessment_validate(const FHIRRiskAssessment* self);

/* ========================================================================== */
/* RiskAssessment-Specific Methods                                           */
/* ========================================================================== */

/**
 * @brief Check if RiskAssessment is active (virtual method)
 * @param self RiskAssessment to check
 * @return true if status is final or amended, false otherwise
 */
bool fhir_riskassessment_is_active(const FHIRRiskAssessment* self);

/**
 * @brief Get RiskAssessment display name (virtual method)
 * @param self RiskAssessment to get name from
 * @return Display name or NULL
 */
const char* fhir_riskassessment_get_display_name(const FHIRRiskAssessment* self);

/**
 * @brief Set RiskAssessment status
 * @param self RiskAssessment to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_riskassessment_set_status(FHIRRiskAssessment* self, FHIRRiskAssessmentStatus status);

/**
 * @brief Add prediction to RiskAssessment
 * @param self RiskAssessment to modify
 * @param prediction Prediction to add
 * @return true on success, false on failure
 */
bool fhir_riskassessment_add_prediction(FHIRRiskAssessment* self, const FHIRRiskAssessmentPrediction* prediction);

/**
 * @brief Get highest risk prediction
 * @param self RiskAssessment to analyze
 * @return Prediction with highest risk or NULL
 */
FHIRRiskAssessmentPrediction* fhir_riskassessment_get_highest_risk_prediction(const FHIRRiskAssessment* self);

/**
 * @brief Check if assessment indicates high risk
 * @param self RiskAssessment to check
 * @param threshold Risk threshold (0.0 to 1.0)
 * @return true if any prediction exceeds threshold, false otherwise
 */
bool fhir_riskassessment_is_high_risk(const FHIRRiskAssessment* self, double threshold);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_riskassessment_status_to_string(FHIRRiskAssessmentStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_RISKASSESSMENT_STATUS_UNKNOWN for invalid string
 */
FHIRRiskAssessmentStatus fhir_riskassessment_status_from_string(const char* status_str);

/**
 * @brief Register RiskAssessment resource type
 * @return true on success, false on failure
 */
bool fhir_riskassessment_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_RISKASSESSMENT_H */