/**
 * @file fhir_careteam.h
 * @brief FHIR R5 CareTeam resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care
 */

#ifndef FHIR_CARETEAM_H
#define FHIR_CARETEAM_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* CareTeam-Specific Enumerations                                            */
/* ========================================================================== */

/**
 * @brief CareTeam status enumeration
 */
typedef enum {
    FHIR_CARETEAM_STATUS_PROPOSED = 0,
    FHIR_CARETEAM_STATUS_ACTIVE,
    FHIR_CARETEAM_STATUS_SUSPENDED,
    FHIR_CARETEAM_STATUS_INACTIVE,
    FHIR_CARETEAM_STATUS_ENTERED_IN_ERROR
} FHIRCareTeamStatus;

/* ========================================================================== */
/* CareTeam Sub-structures                                                   */
/* ========================================================================== */

/**
 * @brief CareTeam participant information
 */
typedef struct FHIRCareTeamParticipant {
    FHIRElement base;
    FHIRCodeableConcept** role;
    size_t role_count;
    FHIRReference* member;
    FHIRReference* on_behalf_of;
    FHIRPeriod* coverage_period;
    FHIRTiming* coverage_timing;
} FHIRCareTeamParticipant;

/* ========================================================================== */
/* CareTeam Resource Structure                                               */
/* ========================================================================== */

/**
 * @brief FHIR R5 CareTeam resource structure
 * 
 * The Care Team includes all the people and organizations who plan to participate
 * in the coordination and delivery of care
 */
FHIR_RESOURCE_DEFINE(CareTeam)
    // CareTeam-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIRCareTeamStatus status;
    
    FHIRCodeableConcept** category;
    size_t category_count;
    
    FHIRString* name;
    
    FHIRReference* subject;
    
    FHIRPeriod* period;
    
    FHIRCareTeamParticipant** participant;
    size_t participant_count;
    
    FHIRCodeableConcept** reason_code;
    size_t reason_code_count;
    
    FHIRReference** reason_reference;
    size_t reason_reference_count;
    
    FHIRReference** managing_organization;
    size_t managing_organization_count;
    
    FHIRContactPoint** telecom;
    size_t telecom_count;
    
    FHIRAnnotation** note;
    size_t note_count;
};

/* ========================================================================== */
/* CareTeam Factory and Lifecycle Methods                                    */
/* ========================================================================== */

/**
 * @brief Create a new CareTeam resource
 * @param id Resource identifier (required)
 * @return Pointer to new CareTeam or NULL on failure
 */
FHIRCareTeam* fhir_careteam_create(const char* id);

/**
 * @brief Destroy CareTeam resource (virtual destructor)
 * @param self CareTeam to destroy
 */
void fhir_careteam_destroy(FHIRCareTeam* self);

/**
 * @brief Clone CareTeam resource (virtual clone)
 * @param self CareTeam to clone
 * @return Cloned CareTeam or NULL on failure
 */
FHIRCareTeam* fhir_careteam_clone(const FHIRCareTeam* self);

/* ========================================================================== */
/* CareTeam Serialization Methods                                            */
/* ========================================================================== */

/**
 * @brief Convert CareTeam to JSON (virtual method)
 * @param self CareTeam to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_careteam_to_json(const FHIRCareTeam* self);

/**
 * @brief Load CareTeam from JSON (virtual method)
 * @param self CareTeam to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_careteam_from_json(FHIRCareTeam* self, const cJSON* json);

/**
 * @brief Parse CareTeam from JSON string
 * @param json_string JSON string
 * @return New CareTeam or NULL on failure
 */
FHIRCareTeam* fhir_careteam_parse(const char* json_string);

/* ========================================================================== */
/* CareTeam Validation Methods                                               */
/* ========================================================================== */

/**
 * @brief Validate CareTeam resource (virtual method)
 * @param self CareTeam to validate
 * @return true if valid, false otherwise
 */
bool fhir_careteam_validate(const FHIRCareTeam* self);

/* ========================================================================== */
/* CareTeam-Specific Methods                                                 */
/* ========================================================================== */

/**
 * @brief Check if CareTeam is active (virtual method)
 * @param self CareTeam to check
 * @return true if status is active, false otherwise
 */
bool fhir_careteam_is_active(const FHIRCareTeam* self);

/**
 * @brief Get CareTeam display name (virtual method)
 * @param self CareTeam to get name from
 * @return Display name or NULL
 */
const char* fhir_careteam_get_display_name(const FHIRCareTeam* self);

/**
 * @brief Set CareTeam status
 * @param self CareTeam to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_careteam_set_status(FHIRCareTeam* self, FHIRCareTeamStatus status);

/**
 * @brief Add participant to CareTeam
 * @param self CareTeam to modify
 * @param participant Participant to add
 * @return true on success, false on failure
 */
bool fhir_careteam_add_participant(FHIRCareTeam* self, const FHIRCareTeamParticipant* participant);

/**
 * @brief Get participants by role
 * @param self CareTeam to search
 * @param role_code Role code to search for
 * @param count Output parameter for result count
 * @return Array of matching participants or NULL
 */
FHIRCareTeamParticipant** fhir_careteam_get_participants_by_role(
    const FHIRCareTeam* self, const char* role_code, size_t* count);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_careteam_status_to_string(FHIRCareTeamStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_CARETEAM_STATUS_PROPOSED for invalid string
 */
FHIRCareTeamStatus fhir_careteam_status_from_string(const char* status_str);

/**
 * @brief Register CareTeam resource type
 * @return true on success, false on failure
 */
bool fhir_careteam_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_CARETEAM_H */