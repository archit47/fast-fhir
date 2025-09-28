/**
 * @file fhir_encounter.c
 * @brief FHIR R5 Encounter resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_encounter.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Encounter, encounter)

/* ========================================================================== */
/* Encounter Sub-structure Methods                                           */
/* ========================================================================== */

FHIREncounterParticipant* fhir_encounter_participant_create(void) {
    FHIREncounterParticipant* participant = fhir_calloc(1, sizeof(FHIREncounterParticipant));
    if (!participant) return NULL;
    
    fhir_element_init(&participant->base);
    return participant;
}

void fhir_encounter_participant_destroy(FHIREncounterParticipant* self) {
    if (!self) return;
    
    fhir_array_destroy((void**)self->type, self->type_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->period) fhir_period_destroy(self->period);
    if (self->individual) fhir_reference_destroy(self->individual);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIREncounterReason* fhir_encounter_reason_create(void) {
    FHIREncounterReason* reason = fhir_calloc(1, sizeof(FHIREncounterReason));
    if (!reason) return NULL;
    
    fhir_element_init(&reason->base);
    return reason;
}

void fhir_encounter_reason_destroy(FHIREncounterReason* self) {
    if (!self) return;
    
    fhir_array_destroy((void**)self->use, self->use_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->value, self->value_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIREncounterDiagnosis* fhir_encounter_diagnosis_create(void) {
    FHIREncounterDiagnosis* diagnosis = fhir_calloc(1, sizeof(FHIREncounterDiagnosis));
    if (!diagnosis) return NULL;
    
    fhir_element_init(&diagnosis->base);
    return diagnosis;
}

void fhir_encounter_diagnosis_destroy(FHIREncounterDiagnosis* self) {
    if (!self) return;
    
    if (self->condition) fhir_reference_destroy(self->condition);
    fhir_array_destroy((void**)self->use, self->use_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIREncounterAdmission* fhir_encounter_admission_create(void) {
    FHIREncounterAdmission* admission = fhir_calloc(1, sizeof(FHIREncounterAdmission));
    if (!admission) return NULL;
    
    fhir_element_init(&admission->base);
    return admission;
}

void fhir_encounter_admission_destroy(FHIREncounterAdmission* self) {
    if (!self) return;
    
    if (self->pre_admission_identifier) fhir_identifier_destroy(self->pre_admission_identifier);
    if (self->origin) fhir_reference_destroy(self->origin);
    if (self->admit_source) fhir_codeableconcept_destroy(self->admit_source);
    if (self->re_admission) fhir_codeableconcept_destroy(self->re_admission);
    if (self->destination) fhir_reference_destroy(self->destination);
    if (self->discharge_disposition) fhir_codeableconcept_destroy(self->discharge_disposition);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIREncounterLocation* fhir_encounter_location_create(void) {
    FHIREncounterLocation* location = fhir_calloc(1, sizeof(FHIREncounterLocation));
    if (!location) return NULL;
    
    fhir_element_init(&location->base);
    location->status = FHIR_ENCOUNTER_LOCATION_STATUS_PLANNED;
    return location;
}

void fhir_encounter_location_destroy(FHIREncounterLocation* self) {
    if (!self) return;
    
    if (self->location) fhir_reference_destroy(self->location);
    if (self->form) fhir_codeableconcept_destroy(self->form);
    if (self->period) fhir_period_destroy(self->period);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

/* ========================================================================== */
/* Encounter Factory and Lifecycle Methods                                   */
/* ========================================================================== */

FHIREncounter* fhir_encounter_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIREncounter* encounter = fhir_calloc(1, sizeof(FHIREncounter));
    if (!encounter) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&encounter->base, &Encounter_vtable, 
                                FHIR_RESOURCE_TYPE_ENCOUNTER, id)) {
        fhir_free(encounter);
        return NULL;
    }
    
    // Initialize Encounter-specific defaults
    encounter->status = FHIR_ENCOUNTER_STATUS_PLANNED;
    encounter->class = FHIR_ENCOUNTER_CLASS_UNKNOWN;
    
    return encounter;
}

void fhir_encounter_destroy(FHIREncounter* self) {
    if (!self) return;
    
    // Free Encounter-specific fields
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    if (self->priority) fhir_codeableconcept_destroy(self->priority);
    fhir_array_destroy((void**)self->type, self->type_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->service_type, self->service_type_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->subject) fhir_reference_destroy(self->subject);
    if (self->subject_status) fhir_reference_destroy(self->subject_status);
    fhir_array_destroy((void**)self->episode_of_care, self->episode_of_care_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->based_on, self->based_on_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->care_team, self->care_team_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->part_of, self->part_of_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->service_provider) fhir_reference_destroy(self->service_provider);
    fhir_array_destroy((void**)self->participant, self->participant_count, (FHIRDestroyFunc)fhir_encounter_participant_destroy);
    fhir_array_destroy((void**)self->appointment, self->appointment_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->virtual_service, self->virtual_service_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->actual_period) fhir_period_destroy(self->actual_period);
    if (self->planned_start_date) fhir_period_destroy(self->planned_start_date);
    if (self->planned_end_date) fhir_period_destroy(self->planned_end_date);
    if (self->length) fhir_duration_destroy(self->length);
    fhir_array_destroy((void**)self->reason, self->reason_count, (FHIRDestroyFunc)fhir_encounter_reason_destroy);
    fhir_array_destroy((void**)self->diagnosis, self->diagnosis_count, (FHIRDestroyFunc)fhir_encounter_diagnosis_destroy);
    fhir_array_destroy((void**)self->account, self->account_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->diet_preference, self->diet_preference_count, (FHIRDestroyFunc)fhir_money_destroy);
    fhir_array_destroy((void**)self->special_arrangement, self->special_arrangement_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->special_courtesy, self->special_courtesy_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->admission) fhir_encounter_admission_destroy(self->admission);
    fhir_array_destroy((void**)self->location, self->location_count, (FHIRDestroyFunc)fhir_encounter_location_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

/* ========================================================================== */
/* Encounter-Specific Methods                                                */
/* ========================================================================== */

bool fhir_encounter_is_active(const FHIREncounter* self) {
    if (!self) return false;
    return self->status == FHIR_ENCOUNTER_STATUS_IN_PROGRESS;
}

bool fhir_encounter_is_completed(const FHIREncounter* self) {
    if (!self) return false;
    return self->status == FHIR_ENCOUNTER_STATUS_COMPLETED ||
           self->status == FHIR_ENCOUNTER_STATUS_DISCHARGED;
}

int fhir_encounter_get_duration_minutes(const FHIREncounter* self) {
    if (!self) return -1;
    
    if (self->length && self->length->value) {
        // Convert duration to minutes based on unit
        // This is a simplified implementation
        return (int)self->length->value->value;
    }
    
    if (self->actual_period && self->actual_period->start && self->actual_period->end) {
        // Calculate duration from actual period
        // This would need proper datetime parsing and calculation
        return -1; // Placeholder
    }
    
    return -1;
}

bool fhir_encounter_set_status(FHIREncounter* self, FHIREncounterStatus status) {
    if (!self) return false;
    
    self->status = status;
    return true;
}

bool fhir_encounter_add_participant(FHIREncounter* self, 
                                   const FHIREncounterParticipant* participant) {
    if (!self || !participant) return false;
    
    return fhir_array_add((void***)&self->participant, &self->participant_count,
                         (void*)participant, sizeof(FHIREncounterParticipant));
}

const char* fhir_encounter_status_to_string(FHIREncounterStatus status) {
    switch (status) {
        case FHIR_ENCOUNTER_STATUS_PLANNED: return "planned";
        case FHIR_ENCOUNTER_STATUS_IN_PROGRESS: return "in-progress";
        case FHIR_ENCOUNTER_STATUS_ON_HOLD: return "on-hold";
        case FHIR_ENCOUNTER_STATUS_DISCHARGED: return "discharged";
        case FHIR_ENCOUNTER_STATUS_COMPLETED: return "completed";
        case FHIR_ENCOUNTER_STATUS_CANCELLED: return "cancelled";
        case FHIR_ENCOUNTER_STATUS_DISCONTINUED: return "discontinued";
        case FHIR_ENCOUNTER_STATUS_ENTERED_IN_ERROR: return "entered-in-error";
        default: return "unknown";
    }
}

FHIREncounterStatus fhir_encounter_status_from_string(const char* status_str) {
    if (!status_str) return FHIR_ENCOUNTER_STATUS_UNKNOWN;
    
    if (strcmp(status_str, "planned") == 0) return FHIR_ENCOUNTER_STATUS_PLANNED;
    if (strcmp(status_str, "in-progress") == 0) return FHIR_ENCOUNTER_STATUS_IN_PROGRESS;
    if (strcmp(status_str, "on-hold") == 0) return FHIR_ENCOUNTER_STATUS_ON_HOLD;
    if (strcmp(status_str, "discharged") == 0) return FHIR_ENCOUNTER_STATUS_DISCHARGED;
    if (strcmp(status_str, "completed") == 0) return FHIR_ENCOUNTER_STATUS_COMPLETED;
    if (strcmp(status_str, "cancelled") == 0) return FHIR_ENCOUNTER_STATUS_CANCELLED;
    if (strcmp(status_str, "discontinued") == 0) return FHIR_ENCOUNTER_STATUS_DISCONTINUED;
    if (strcmp(status_str, "entered-in-error") == 0) return FHIR_ENCOUNTER_STATUS_ENTERED_IN_ERROR;
    
    return FHIR_ENCOUNTER_STATUS_UNKNOWN;
}

bool fhir_encounter_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_ENCOUNTER,
        .name = "Encounter",
        .vtable = &Encounter_vtable,
        .factory = (FHIRResourceFactory)fhir_encounter_create
    };
    
    return fhir_resource_register_type(&registration);
}