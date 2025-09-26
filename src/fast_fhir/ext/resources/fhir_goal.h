/**
 * @file fhir_goal.h
 * @brief FHIR R5 Goal resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * Describes the intended objective(s) for a patient, group or organization care
 */

#ifndef FHIR_GOAL_H
#define FHIR_GOAL_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Goal-Specific Enumerations                                                */
/* ========================================================================== */

/**
 * @brief Goal lifecycle status enumeration
 */
typedef enum {
    FHIR_GOAL_STATUS_PROPOSED = 0,
    FHIR_GOAL_STATUS_PLANNED,
    FHIR_GOAL_STATUS_ACCEPTED,
    FHIR_GOAL_STATUS_ACTIVE,
    FHIR_GOAL_STATUS_ON_HOLD,
    FHIR_GOAL_STATUS_COMPLETED,
    FHIR_GOAL_STATUS_CANCELLED,
    FHIR_GOAL_STATUS_ENTERED_IN_ERROR,
    FHIR_GOAL_STATUS_REJECTED
} FHIRGoalStatus;

/**
 * @brief Goal achievement status enumeration
 */
typedef enum {
    FHIR_GOAL_ACHIEVEMENT_IN_PROGRESS = 0,
    FHIR_GOAL_ACHIEVEMENT_IMPROVING,
    FHIR_GOAL_ACHIEVEMENT_WORSENING,
    FHIR_GOAL_ACHIEVEMENT_NO_CHANGE,
    FHIR_GOAL_ACHIEVEMENT_ACHIEVED,
    FHIR_GOAL_ACHIEVEMENT_SUSTAINING,
    FHIR_GOAL_ACHIEVEMENT_NOT_ACHIEVED,
    FHIR_GOAL_ACHIEVEMENT_NO_PROGRESS,
    FHIR_GOAL_ACHIEVEMENT_NOT_ATTAINABLE
} FHIRGoalAchievementStatus;

/* ========================================================================== */
/* Goal Sub-structures                                                       */
/* ========================================================================== */

/**
 * @brief Goal target information
 */
typedef struct FHIRGoalTarget {
    FHIRElement base;
    FHIRCodeableConcept* measure;
    
    // Detail (choice type)
    FHIRQuantity* detail_quantity;
    FHIRRange* detail_range;
    FHIRCodeableConcept* detail_codeable_concept;
    FHIRString* detail_string;
    FHIRBoolean* detail_boolean;
    FHIRInteger* detail_integer;
    FHIRRatio* detail_ratio;
    
    // Due (choice type)
    FHIRDate* due_date;
    FHIRDuration* due_duration;
} FHIRGoalTarget;

/* ========================================================================== */
/* Goal Resource Structure                                                   */
/* ========================================================================== */

/**
 * @brief FHIR R5 Goal resource structure
 * 
 * Describes the intended objective(s) for a patient, group or organization care
 */
FHIR_RESOURCE_DEFINE(Goal)
    // Goal-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRGoalStatus lifecycle_status;
    
    FHIRCodeableConcept* achievement_status;
    
    FHIRCodeableConcept** category;
    size_t category_count;
    
    FHIRBoolean* continuous;
    
    FHIRCodeableConcept* priority;
    
    FHIRCodeableConcept* description;
    
    FHIRReference* subject;
    
    // Start (choice type)
    FHIRDate* start_date;
    FHIRCodeableConcept* start_codeable_concept;
    
    FHIRGoalTarget** target;
    size_t target_count;
    
    FHIRDate* status_date;
    
    FHIRString* status_reason;
    
    FHIRReference* source;
    
    FHIRReference** addresses;
    size_t addresses_count;
    
    FHIRAnnotation** note;
    size_t note_count;
    
    FHIRCodeableConcept** outcome_code;
    size_t outcome_code_count;
    
    FHIRReference** outcome_reference;
    size_t outcome_reference_count;
};

/* ========================================================================== */
/* Goal Factory and Lifecycle Methods                                        */
/* ========================================================================== */

/**
 * @brief Create a new Goal resource
 * @param id Resource identifier (required)
 * @return Pointer to new Goal or NULL on failure
 */
FHIRGoal* fhir_goal_create(const char* id);

/**
 * @brief Destroy Goal resource (virtual destructor)
 * @param self Goal to destroy
 */
void fhir_goal_destroy(FHIRGoal* self);

/**
 * @brief Clone Goal resource (virtual clone)
 * @param self Goal to clone
 * @return Cloned Goal or NULL on failure
 */
FHIRGoal* fhir_goal_clone(const FHIRGoal* self);

/* ========================================================================== */
/* Goal Serialization Methods                                                */
/* ========================================================================== */

/**
 * @brief Convert Goal to JSON (virtual method)
 * @param self Goal to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_goal_to_json(const FHIRGoal* self);

/**
 * @brief Load Goal from JSON (virtual method)
 * @param self Goal to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_goal_from_json(FHIRGoal* self, const cJSON* json);

/**
 * @brief Parse Goal from JSON string
 * @param json_string JSON string
 * @return New Goal or NULL on failure
 */
FHIRGoal* fhir_goal_parse(const char* json_string);

/* ========================================================================== */
/* Goal Validation Methods                                                   */
/* ========================================================================== */

/**
 * @brief Validate Goal resource (virtual method)
 * @param self Goal to validate
 * @return true if valid, false otherwise
 */
bool fhir_goal_validate(const FHIRGoal* self);

/* ========================================================================== */
/* Goal-Specific Methods                                                     */
/* ========================================================================== */

/**
 * @brief Check if Goal is active (virtual method)
 * @param self Goal to check
 * @return true if status is active, false otherwise
 */
bool fhir_goal_is_active(const FHIRGoal* self);

/**
 * @brief Get Goal display name (virtual method)
 * @param self Goal to get name from
 * @return Display name or NULL
 */
const char* fhir_goal_get_display_name(const FHIRGoal* self);

/**
 * @brief Set Goal lifecycle status
 * @param self Goal to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_goal_set_lifecycle_status(FHIRGoal* self, FHIRGoalStatus status);

/**
 * @brief Set Goal achievement status
 * @param self Goal to modify
 * @param achievement_status New achievement status
 * @return true on success, false on failure
 */
bool fhir_goal_set_achievement_status(FHIRGoal* self, FHIRGoalAchievementStatus achievement_status);

/**
 * @brief Add target to Goal
 * @param self Goal to modify
 * @param target Target to add
 * @return true on success, false on failure
 */
bool fhir_goal_add_target(FHIRGoal* self, const FHIRGoalTarget* target);

/**
 * @brief Check if Goal is achieved
 * @param self Goal to check
 * @return true if goal is achieved, false otherwise
 */
bool fhir_goal_is_achieved(const FHIRGoal* self);

/**
 * @brief Convert lifecycle status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_goal_status_to_string(FHIRGoalStatus status);

/**
 * @brief Convert string to lifecycle status enum
 * @param status_str String representation
 * @return Status enum or FHIR_GOAL_STATUS_PROPOSED for invalid string
 */
FHIRGoalStatus fhir_goal_status_from_string(const char* status_str);

/**
 * @brief Convert achievement status enum to string
 * @param achievement_status Achievement status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_goal_achievement_status_to_string(FHIRGoalAchievementStatus achievement_status);

/**
 * @brief Convert string to achievement status enum
 * @param achievement_str String representation
 * @return Achievement status enum or FHIR_GOAL_ACHIEVEMENT_IN_PROGRESS for invalid string
 */
FHIRGoalAchievementStatus fhir_goal_achievement_status_from_string(const char* achievement_str);

/**
 * @brief Register Goal resource type
 * @return true on success, false on failure
 */
bool fhir_goal_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_GOAL_H */