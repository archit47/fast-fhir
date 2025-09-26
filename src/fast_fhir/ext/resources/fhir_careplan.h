/**
 * @file fhir_careplan.h
 * @brief FHIR R5 CarePlan resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community
 */

#ifndef FHIR_CAREPLAN_H
#define FHIR_CAREPLAN_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* CarePlan-Specific Enumerations                                            */
/* ========================================================================== */

/**
 * @brief CarePlan status enumeration
 */
typedef enum {
    FHIR_CAREPLAN_STATUS_DRAFT = 0,
    FHIR_CAREPLAN_STATUS_ACTIVE,
    FHIR_CAREPLAN_STATUS_ON_HOLD,
    FHIR_CAREPLAN_STATUS_REVOKED,
    FHIR_CAREPLAN_STATUS_COMPLETED,
    FHIR_CAREPLAN_STATUS_ENTERED_IN_ERROR,
    FHIR_CAREPLAN_STATUS_UNKNOWN
} FHIRCarePlanStatus;

/**
 * @brief CarePlan intent enumeration
 */
typedef enum {
    FHIR_CAREPLAN_INTENT_PROPOSAL = 0,
    FHIR_CAREPLAN_INTENT_PLAN,
    FHIR_CAREPLAN_INTENT_ORDER,
    FHIR_CAREPLAN_INTENT_OPTION,
    FHIR_CAREPLAN_INTENT_DIRECTIVE
} FHIRCarePlanIntent;

/**
 * @brief CarePlan activity status enumeration
 */
typedef enum {
    FHIR_CAREPLAN_ACTIVITY_STATUS_NOT_STARTED = 0,
    FHIR_CAREPLAN_ACTIVITY_STATUS_SCHEDULED,
    FHIR_CAREPLAN_ACTIVITY_STATUS_IN_PROGRESS,
    FHIR_CAREPLAN_ACTIVITY_STATUS_ON_HOLD,
    FHIR_CAREPLAN_ACTIVITY_STATUS_COMPLETED,
    FHIR_CAREPLAN_ACTIVITY_STATUS_CANCELLED,
    FHIR_CAREPLAN_ACTIVITY_STATUS_STOPPED,
    FHIR_CAREPLAN_ACTIVITY_STATUS_UNKNOWN,
    FHIR_CAREPLAN_ACTIVITY_STATUS_ENTERED_IN_ERROR
} FHIRCarePlanActivityStatus;

/* ========================================================================== */
/* CarePlan Sub-structures                                                   */
/* ========================================================================== */

/**
 * @brief CarePlan activity detail information
 */
typedef struct FHIRCarePlanActivityDetail {
    FHIRElement base;
    FHIRCodeableConcept* kind;
    FHIRReference** instantiates_canonical;
    size_t instantiates_canonical_count;
    FHIRReference** instantiates_uri;
    size_t instantiates_uri_count;
    FHIRCodeableConcept* code;
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    FHIRReference** goal;
    size_t goal_count;
    FHIRCarePlanActivityStatus status;
    FHIRCodeableConcept* status_reason;
    FHIRBoolean* do_not_perform;
    FHIRTiming* scheduled_timing;
    FHIRPeriod* scheduled_period;
    FHIRString* scheduled_string;
    FHIRReference* location;
    FHIRCodeableConcept** reported_boolean;
    size_t reported_boolean_count;
    FHIRReference* reported_reference;
    FHIRReference** performer;
    size_t performer_count;
    FHIRCodeableConcept* product_codeable_concept;
    FHIRReference* product_reference;
    FHIRQuantity* daily_amount;
    FHIRQuantity* quantity;
    FHIRString* description;
} FHIRCarePlanActivityDetail;

/**
 * @brief CarePlan activity information
 */
typedef struct FHIRCarePlanActivity {
    FHIRElement base;
    FHIRCodeableConcept** outcome_codeable_concept;
    size_t outcome_codeable_concept_count;
    FHIRReference** outcome_reference;
    size_t outcome_reference_count;
    FHIRAnnotation** progress;
    size_t progress_count;
    FHIRReference* reference;
    FHIRCarePlanActivityDetail* detail;
} FHIRCarePlanActivity;

/* ========================================================================== */
/* CarePlan Resource Structure                                               */
/* ========================================================================== */

/**
 * @brief FHIR R5 CarePlan resource structure
 * 
 * Describes the intention of how one or more practitioners intend to deliver care
 */
FHIR_RESOURCE_DEFINE(CarePlan)
    // CarePlan-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRReference** instantiates_canonical;
    size_t instantiates_canonical_count;
    
    FHIRReference** instantiates_uri;
    size_t instantiates_uri_count;
    
    FHIRReference** based_on;
    size_t based_on_count;
    
    FHIRReference** replaces;
    size_t replaces_count;
    
    FHIRReference** part_of;
    size_t part_of_count;
    
    FHIRCarePlanStatus status;
    
    FHIRCarePlanIntent intent;
    
    FHIRCodeableConcept** category;
    size_t category_count;
    
    FHIRString* title;
    
    FHIRString* description;
    
    FHIRReference* subject;
    
    FHIRReference* encounter;
    
    FHIRPeriod* period;
    
    FHIRDateTime* created;
    
    FHIRReference** custodian;
    size_t custodian_count;
    
    FHIRReference** contributor;
    size_t contributor_count;
    
    FHIRReference** care_team;
    size_t care_team_count;
    
    FHIRReference** addresses;
    size_t addresses_count;
    
    FHIRReference** supporting_info;
    size_t supporting_info_count;
    
    FHIRReference** goal;
    size_t goal_count;
    
    FHIRCarePlanActivity** activity;
    size_t activity_count;
    
    FHIRAnnotation** note;
    size_t note_count;
};

/* ========================================================================== */
/* CarePlan Factory and Lifecycle Methods                                    */
/* ========================================================================== */

/**
 * @brief Create a new CarePlan resource
 * @param id Resource identifier (required)
 * @return Pointer to new CarePlan or NULL on failure
 */
FHIRCarePlan* fhir_careplan_create(const char* id);

/**
 * @brief Destroy CarePlan resource (virtual destructor)
 * @param self CarePlan to destroy
 */
void fhir_careplan_destroy(FHIRCarePlan* self);

/**
 * @brief Clone CarePlan resource (virtual clone)
 * @param self CarePlan to clone
 * @return Cloned CarePlan or NULL on failure
 */
FHIRCarePlan* fhir_careplan_clone(const FHIRCarePlan* self);

/* ========================================================================== */
/* CarePlan Serialization Methods                                            */
/* ========================================================================== */

/**
 * @brief Convert CarePlan to JSON (virtual method)
 * @param self CarePlan to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_careplan_to_json(const FHIRCarePlan* self);

/**
 * @brief Load CarePlan from JSON (virtual method)
 * @param self CarePlan to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_careplan_from_json(FHIRCarePlan* self, const cJSON* json);

/**
 * @brief Parse CarePlan from JSON string
 * @param json_string JSON string
 * @return New CarePlan or NULL on failure
 */
FHIRCarePlan* fhir_careplan_parse(const char* json_string);

/* ========================================================================== */
/* CarePlan Validation Methods                                               */
/* ========================================================================== */

/**
 * @brief Validate CarePlan resource (virtual method)
 * @param self CarePlan to validate
 * @return true if valid, false otherwise
 */
bool fhir_careplan_validate(const FHIRCarePlan* self);

/* ========================================================================== */
/* CarePlan-Specific Methods                                                 */
/* ========================================================================== */

/**
 * @brief Check if CarePlan is active (virtual method)
 * @param self CarePlan to check
 * @return true if status is active, false otherwise
 */
bool fhir_careplan_is_active(const FHIRCarePlan* self);

/**
 * @brief Get CarePlan display name (virtual method)
 * @param self CarePlan to get name from
 * @return Display name or NULL
 */
const char* fhir_careplan_get_display_name(const FHIRCarePlan* self);

/**
 * @brief Set CarePlan status
 * @param self CarePlan to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_careplan_set_status(FHIRCarePlan* self, FHIRCarePlanStatus status);

/**
 * @brief Set CarePlan intent
 * @param self CarePlan to modify
 * @param intent New intent
 * @return true on success, false on failure
 */
bool fhir_careplan_set_intent(FHIRCarePlan* self, FHIRCarePlanIntent intent);

/**
 * @brief Add activity to CarePlan
 * @param self CarePlan to modify
 * @param activity Activity to add
 * @return true on success, false on failure
 */
bool fhir_careplan_add_activity(FHIRCarePlan* self, const FHIRCarePlanActivity* activity);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_careplan_status_to_string(FHIRCarePlanStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_CAREPLAN_STATUS_UNKNOWN for invalid string
 */
FHIRCarePlanStatus fhir_careplan_status_from_string(const char* status_str);

/**
 * @brief Convert intent enum to string
 * @param intent Intent enum
 * @return String representation or NULL for unknown intent
 */
const char* fhir_careplan_intent_to_string(FHIRCarePlanIntent intent);

/**
 * @brief Convert string to intent enum
 * @param intent_str String representation
 * @return Intent enum or FHIR_CAREPLAN_INTENT_PROPOSAL for invalid string
 */
FHIRCarePlanIntent fhir_careplan_intent_from_string(const char* intent_str);

/**
 * @brief Register CarePlan resource type
 * @return true on success, false on failure
 */
bool fhir_careplan_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_CAREPLAN_H */