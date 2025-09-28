/**
 * @file fhir_encounter.h
 * @brief FHIR R5 Encounter resource C interface with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#ifndef FHIR_ENCOUNTER_H
#define FHIR_ENCOUNTER_H

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Encounter-Specific Enumerations                                           */
/* ========================================================================== */

/**
 * @brief Encounter status enumeration
 */
typedef enum {
    FHIR_ENCOUNTER_STATUS_UNKNOWN = 0,
    FHIR_ENCOUNTER_STATUS_PLANNED,
    FHIR_ENCOUNTER_STATUS_IN_PROGRESS,
    FHIR_ENCOUNTER_STATUS_ON_HOLD,
    FHIR_ENCOUNTER_STATUS_DISCHARGED,
    FHIR_ENCOUNTER_STATUS_COMPLETED,
    FHIR_ENCOUNTER_STATUS_CANCELLED,
    FHIR_ENCOUNTER_STATUS_DISCONTINUED,
    FHIR_ENCOUNTER_STATUS_ENTERED_IN_ERROR
} FHIREncounterStatus;

/**
 * @brief Encounter class enumeration
 */
typedef enum {
    FHIR_ENCOUNTER_CLASS_UNKNOWN = 0,
    FHIR_ENCOUNTER_CLASS_AMBULATORY,
    FHIR_ENCOUNTER_CLASS_EMERGENCY,
    FHIR_ENCOUNTER_CLASS_FIELD,
    FHIR_ENCOUNTER_CLASS_HOME_HEALTH,
    FHIR_ENCOUNTER_CLASS_INPATIENT,
    FHIR_ENCOUNTER_CLASS_OBSERVATION,
    FHIR_ENCOUNTER_CLASS_OUTPATIENT,
    FHIR_ENCOUNTER_CLASS_VIRTUAL
} FHIREncounterClass;

/**
 * @brief Encounter location status enumeration
 */
typedef enum {
    FHIR_ENCOUNTER_LOCATION_STATUS_PLANNED,
    FHIR_ENCOUNTER_LOCATION_STATUS_ACTIVE,
    FHIR_ENCOUNTER_LOCATION_STATUS_RESERVED,
    FHIR_ENCOUNTER_LOCATION_STATUS_COMPLETED
} FHIREncounterLocationStatus;

/* ========================================================================== */
/* Encounter Sub-structures                                                  */
/* ========================================================================== */

/**
 * @brief Encounter participant information
 */
typedef struct FHIREncounterParticipant {
    FHIRElement base;
    FHIRCodeableConcept** type;
    size_t type_count;
    FHIRPeriod* period;
    FHIRReference* individual;
} FHIREncounterParticipant;

/**
 * @brief Encounter reason information
 */
typedef struct FHIREncounterReason {
    FHIRElement base;
    FHIRCodeableConcept** use;
    size_t use_count;
    FHIRCodeableConcept** value;
    size_t value_count;
} FHIREncounterReason;

/**
 * @brief Encounter diagnosis information
 */
typedef struct FHIREncounterDiagnosis {
    FHIRElement base;
    FHIRReference* condition;
    FHIRCodeableConcept** use;
    size_t use_count;
} FHIREncounterDiagnosis;

/**
 * @brief Encounter admission information
 */
typedef struct FHIREncounterAdmission {
    FHIRElement base;
    FHIRIdentifier* pre_admission_identifier;
    FHIRReference* origin;
    FHIRCodeableConcept* admit_source;
    FHIRCodeableConcept* re_admission;
    FHIRReference* destination;
    FHIRCodeableConcept* discharge_disposition;
} FHIREncounterAdmission;

/**
 * @brief Encounter location information
 */
typedef struct FHIREncounterLocation {
    FHIRElement base;
    FHIRReference* location;
    FHIREncounterLocationStatus status;
    FHIRCodeableConcept* form;
    FHIRPeriod* period;
} FHIREncounterLocation;

/* ========================================================================== */
/* Encounter Resource Structure                                              */
/* ========================================================================== */

/**
 * @brief FHIR R5 Encounter resource structure
 * 
 * An interaction between a patient and healthcare provider(s) for the purpose
 * of providing healthcare service(s) or assessing the health status of a patient.
 */
FHIR_RESOURCE_DEFINE(Encounter)
    // Encounter-specific fields
    FHIRIdentifier** identifier;
    size_t identifier_count;
    
    FHIREncounterStatus status;
    
    FHIREncounterClass class;
    
    FHIRCodeableConcept* priority;
    
    FHIRCodeableConcept** type;
    size_t type_count;
    
    FHIRCodeableConcept** service_type;
    size_t service_type_count;
    
    FHIRReference* subject;
    
    FHIRReference* subject_status;
    
    FHIRReference** episode_of_care;
    size_t episode_of_care_count;
    
    FHIRReference** based_on;
    size_t based_on_count;
    
    FHIRReference** care_team;
    size_t care_team_count;
    
    FHIRReference** part_of;
    size_t part_of_count;
    
    FHIRReference* service_provider;
    
    FHIREncounterParticipant** participant;
    size_t participant_count;
    
    FHIRReference** appointment;
    size_t appointment_count;
    
    FHIRReference** virtual_service;
    size_t virtual_service_count;
    
    FHIRPeriod* actual_period;
    
    FHIRPeriod* planned_start_date;
    
    FHIRPeriod* planned_end_date;
    
    FHIRDuration* length;
    
    FHIREncounterReason** reason;
    size_t reason_count;
    
    FHIREncounterDiagnosis** diagnosis;
    size_t diagnosis_count;
    
    FHIRReference** account;
    size_t account_count;
    
    FHIRMoney** diet_preference;
    size_t diet_preference_count;
    
    FHIRCodeableConcept** special_arrangement;
    size_t special_arrangement_count;
    
    FHIRCodeableConcept** special_courtesy;
    size_t special_courtesy_count;
    
    FHIREncounterAdmission* admission;
    
    FHIREncounterLocation** location;
    size_t location_count;
};

/* ========================================================================== */
/* Encounter Factory and Lifecycle Methods                                   */
/* ========================================================================== */

/**
 * @brief Create a new Encounter resource
 * @param id Resource identifier (required)
 * @return Pointer to new Encounter or NULL on failure
 */
FHIREncounter* fhir_encounter_create(const char* id);

/**
 * @brief Destroy Encounter resource (virtual destructor)
 * @param self Encounter to destroy
 */
void fhir_encounter_destroy(FHIREncounter* self);

/* ========================================================================== */
/* Encounter-Specific Methods                                                */
/* ========================================================================== */

/**
 * @brief Check if Encounter is active
 * @param self Encounter to check
 * @return true if active (in-progress), false otherwise
 */
bool fhir_encounter_is_active(const FHIREncounter* self);

/**
 * @brief Check if Encounter is completed
 * @param self Encounter to check
 * @return true if completed, false otherwise
 */
bool fhir_encounter_is_completed(const FHIREncounter* self);

/**
 * @brief Get Encounter duration in minutes
 * @param self Encounter to calculate duration for
 * @return Duration in minutes or -1 if not available
 */
int fhir_encounter_get_duration_minutes(const FHIREncounter* self);

/**
 * @brief Set Encounter status
 * @param self Encounter to modify
 * @param status New status
 * @return true on success, false on failure
 */
bool fhir_encounter_set_status(FHIREncounter* self, FHIREncounterStatus status);

/**
 * @brief Add participant to Encounter
 * @param self Encounter to modify
 * @param participant Participant to add
 * @return true on success, false on failure
 */
bool fhir_encounter_add_participant(FHIREncounter* self, 
                                   const FHIREncounterParticipant* participant);

/**
 * @brief Convert status enum to string
 * @param status Status enum
 * @return String representation or NULL for unknown status
 */
const char* fhir_encounter_status_to_string(FHIREncounterStatus status);

/**
 * @brief Convert string to status enum
 * @param status_str String representation
 * @return Status enum or FHIR_ENCOUNTER_STATUS_UNKNOWN for invalid string
 */
FHIREncounterStatus fhir_encounter_status_from_string(const char* status_str);

/**
 * @brief Register Encounter resource type
 * @return true on success, false on failure
 */
bool fhir_encounter_register(void);

#ifdef __cplusplus
}
#endif

#endif /* FHIR_ENCOUNTER_H */