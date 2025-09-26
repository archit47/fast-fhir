/**
 * @file fhir_careplan.c
 * @brief FHIR R5 CarePlan resource C implementation with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "fhir_careplan.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(CarePlan, careplan)

/* ========================================================================== */
/* CarePlan Sub-structure Methods                                            */
/* ========================================================================== */

FHIRCarePlanActivityDetail* fhir_careplan_activity_detail_create(void) {
    FHIRCarePlanActivityDetail* detail = fhir_calloc(1, sizeof(FHIRCarePlanActivityDetail));
    if (!detail) return NULL;
    
    fhir_element_init(&detail->base);
    detail->status = FHIR_CAREPLAN_ACTIVITY_STATUS_NOT_STARTED;
    return detail;
}

void fhir_careplan_activity_detail_destroy(FHIRCarePlanActivityDetail* self) {
    if (!self) return;
    
    if (self->kind) fhir_codeableconcept_destroy(self->kind);
    fhir_array_destroy((void**)self->instantiates_canonical, self->instantiates_canonical_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->instantiates_uri, self->instantiates_uri_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->code) fhir_codeableconcept_destroy(self->code);
    fhir_array_destroy((void**)self->reason_code, self->reason_code_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->reason_reference, self->reason_reference_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->goal, self->goal_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->status_reason) fhir_codeableconcept_destroy(self->status_reason);
    if (self->do_not_perform) fhir_boolean_destroy(self->do_not_perform);
    if (self->scheduled_timing) fhir_timing_destroy(self->scheduled_timing);
    if (self->scheduled_period) fhir_period_destroy(self->scheduled_period);
    if (self->scheduled_string) fhir_string_destroy(self->scheduled_string);
    if (self->location) fhir_reference_destroy(self->location);
    fhir_array_destroy((void**)self->reported_boolean, self->reported_boolean_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->reported_reference) fhir_reference_destroy(self->reported_reference);
    fhir_array_destroy((void**)self->performer, self->performer_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->product_codeable_concept) fhir_codeableconcept_destroy(self->product_codeable_concept);
    if (self->product_reference) fhir_reference_destroy(self->product_reference);
    if (self->daily_amount) fhir_quantity_destroy(self->daily_amount);
    if (self->quantity) fhir_quantity_destroy(self->quantity);
    if (self->description) fhir_string_destroy(self->description);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIRCarePlanActivity* fhir_careplan_activity_create(void) {
    FHIRCarePlanActivity* activity = fhir_calloc(1, sizeof(FHIRCarePlanActivity));
    if (!activity) return NULL;
    
    fhir_element_init(&activity->base);
    return activity;
}

void fhir_careplan_activity_destroy(FHIRCarePlanActivity* self) {
    if (!self) return;
    
    fhir_array_destroy((void**)self->outcome_codeable_concept, self->outcome_codeable_concept_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->outcome_reference, self->outcome_reference_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->progress, self->progress_count, (FHIRDestroyFunc)fhir_annotation_destroy);
    if (self->reference) fhir_reference_destroy(self->reference);
    if (self->detail) fhir_careplan_activity_detail_destroy(self->detail);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

/* ========================================================================== */
/* CarePlan Factory and Lifecycle Methods                                    */
/* ========================================================================== */

FHIRCarePlan* fhir_careplan_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRCarePlan* careplan = fhir_calloc(1, sizeof(FHIRCarePlan));
    if (!careplan) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&careplan->base, &CarePlan_vtable, 
                                FHIR_RESOURCE_TYPE_CAREPLAN, id)) {
        fhir_free(careplan);
        return NULL;
    }
    
    // Initialize CarePlan-specific defaults
    careplan->status = FHIR_CAREPLAN_STATUS_DRAFT;
    careplan->intent = FHIR_CAREPLAN_INTENT_PLAN;
    
    return careplan;
}

void fhir_careplan_destroy(FHIRCarePlan* self) {
    if (!self) return;
    
    // Free CarePlan-specific fields
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    fhir_array_destroy((void**)self->instantiates_canonical, self->instantiates_canonical_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->instantiates_uri, self->instantiates_uri_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->based_on, self->based_on_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->replaces, self->replaces_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->part_of, self->part_of_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->category, self->category_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->title) fhir_string_destroy(self->title);
    if (self->description) fhir_string_destroy(self->description);
    if (self->subject) fhir_reference_destroy(self->subject);
    if (self->encounter) fhir_reference_destroy(self->encounter);
    if (self->period) fhir_period_destroy(self->period);
    if (self->created) fhir_datetime_destroy(self->created);
    fhir_array_destroy((void**)self->custodian, self->custodian_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->contributor, self->contributor_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->care_team, self->care_team_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->addresses, self->addresses_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->supporting_info, self->supporting_info_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->goal, self->goal_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->activity, self->activity_count, (FHIRDestroyFunc)fhir_careplan_activity_destroy);
    fhir_array_destroy((void**)self->note, self->note_count, (FHIRDestroyFunc)fhir_annotation_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRCarePlan* fhir_careplan_clone(const FHIRCarePlan* self) {
    if (!self) return NULL;
    
    FHIRCarePlan* clone = fhir_careplan_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone CarePlan-specific fields
    clone->status = self->status;
    clone->intent = self->intent;
    
    clone->identifier = fhir_array_clone((void**)self->identifier, self->identifier_count, 
                                        (FHIRCloneFunc)fhir_identifier_clone, &clone->identifier_count);
    
    clone->category = fhir_array_clone((void**)self->category, self->category_count, 
                                      (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->category_count);
    
    if (self->title) {
        clone->title = fhir_string_clone(self->title);
    }
    
    if (self->description) {
        clone->description = fhir_string_clone(self->description);
    }
    
    if (self->subject) {
        clone->subject = fhir_reference_clone(self->subject);
    }
    
    if (self->encounter) {
        clone->encounter = fhir_reference_clone(self->encounter);
    }
    
    if (self->period) {
        clone->period = fhir_period_clone(self->period);
    }
    
    if (self->created) {
        clone->created = fhir_datetime_clone(self->created);
    }
    
    clone->goal = fhir_array_clone((void**)self->goal, self->goal_count, 
                                  (FHIRCloneFunc)fhir_reference_clone, &clone->goal_count);
    
    return clone;
}

/* ========================================================================== */
/* CarePlan Serialization Methods                                            */
/* ========================================================================== */

cJSON* fhir_careplan_to_json(const FHIRCarePlan* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "CarePlan is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "CarePlan") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add status and intent
    const char* status_str = fhir_careplan_status_to_string(self->status);
    fhir_json_add_string(json, "status", status_str);
    
    const char* intent_str = fhir_careplan_intent_to_string(self->intent);
    fhir_json_add_string(json, "intent", intent_str);
    
    // Add CarePlan-specific fields
    if (self->identifier && self->identifier_count > 0) {
        fhir_json_add_identifier_array(json, "identifier", self->identifier, self->identifier_count);
    }
    
    if (self->category && self->category_count > 0) {
        fhir_json_add_codeableconcept_array(json, "category", self->category, self->category_count);
    }
    
    if (self->title) {
        fhir_json_add_string_value(json, "title", self->title);
    }
    
    if (self->description) {
        fhir_json_add_string_value(json, "description", self->description);
    }
    
    if (self->subject) {
        fhir_json_add_reference(json, "subject", self->subject);
    }
    
    if (self->encounter) {
        fhir_json_add_reference(json, "encounter", self->encounter);
    }
    
    if (self->period) {
        fhir_json_add_period(json, "period", self->period);
    }
    
    if (self->created) {
        fhir_json_add_datetime(json, "created", self->created);
    }
    
    if (self->goal && self->goal_count > 0) {
        fhir_json_add_reference_array(json, "goal", self->goal, self->goal_count);
    }
    
    if (self->care_team && self->care_team_count > 0) {
        fhir_json_add_reference_array(json, "careTeam", self->care_team, self->care_team_count);
    }
    
    return json;
}

bool fhir_careplan_from_json(FHIRCarePlan* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "CarePlan") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse status and intent
    const char* status_str = fhir_json_get_string(json, "status");
    if (status_str) {
        self->status = fhir_careplan_status_from_string(status_str);
    }
    
    const char* intent_str = fhir_json_get_string(json, "intent");
    if (intent_str) {
        self->intent = fhir_careplan_intent_from_string(intent_str);
    }
    
    // Parse CarePlan-specific fields
    const cJSON* identifier_json = cJSON_GetObjectItem(json, "identifier");
    if (identifier_json && cJSON_IsArray(identifier_json)) {
        self->identifier = fhir_json_parse_identifier_array(identifier_json, &self->identifier_count);
    }
    
    const cJSON* category_json = cJSON_GetObjectItem(json, "category");
    if (category_json && cJSON_IsArray(category_json)) {
        self->category = fhir_json_parse_codeableconcept_array(category_json, &self->category_count);
    }
    
    const cJSON* title_json = cJSON_GetObjectItem(json, "title");
    if (title_json) {
        self->title = fhir_json_parse_string(title_json);
    }
    
    const cJSON* description_json = cJSON_GetObjectItem(json, "description");
    if (description_json) {
        self->description = fhir_json_parse_string(description_json);
    }
    
    const cJSON* subject_json = cJSON_GetObjectItem(json, "subject");
    if (subject_json) {
        self->subject = fhir_json_parse_reference(subject_json);
    }
    
    const cJSON* encounter_json = cJSON_GetObjectItem(json, "encounter");
    if (encounter_json) {
        self->encounter = fhir_json_parse_reference(encounter_json);
    }
    
    const cJSON* period_json = cJSON_GetObjectItem(json, "period");
    if (period_json) {
        self->period = fhir_json_parse_period(period_json);
    }
    
    const cJSON* created_json = cJSON_GetObjectItem(json, "created");
    if (created_json) {
        self->created = fhir_json_parse_datetime(created_json);
    }
    
    const cJSON* goal_json = cJSON_GetObjectItem(json, "goal");
    if (goal_json && cJSON_IsArray(goal_json)) {
        self->goal = fhir_json_parse_reference_array(goal_json, &self->goal_count);
    }
    
    return true;
}

FHIRCarePlan* fhir_careplan_parse(const char* json_string) {
    if (!json_string) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "JSON string is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_JSON, "Failed to parse JSON");
        return NULL;
    }
    
    const char* id = fhir_json_get_string(json, "id");
    if (!id) {
        cJSON_Delete(json);
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "id");
        return NULL;
    }
    
    FHIRCarePlan* careplan = fhir_careplan_create(id);
    if (!careplan) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_careplan_from_json(careplan, json)) {
        fhir_careplan_destroy(careplan);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return careplan;
}

/* ========================================================================== */
/* CarePlan Validation Methods                                               */
/* ========================================================================== */

bool fhir_careplan_validate(const FHIRCarePlan* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("CarePlan", self->base.id)) {
        return false;
    }
    
    // Validate required fields
    if (!self->subject) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "subject");
        return false;
    }
    
    return true;
}

/* ========================================================================== */
/* CarePlan-Specific Methods                                                 */
/* ========================================================================== */

bool fhir_careplan_is_active(const FHIRCarePlan* self) {
    if (!self) return false;
    return self->status == FHIR_CAREPLAN_STATUS_ACTIVE;
}

const char* fhir_careplan_get_display_name(const FHIRCarePlan* self) {
    if (!self) return NULL;
    
    // Return title if available
    if (self->title && self->title->value) {
        return self->title->value;
    }
    
    return "CarePlan";
}

bool fhir_careplan_set_status(FHIRCarePlan* self, FHIRCarePlanStatus status) {
    if (!self) return false;
    
    self->status = status;
    return true;
}

bool fhir_careplan_set_intent(FHIRCarePlan* self, FHIRCarePlanIntent intent) {
    if (!self) return false;
    
    self->intent = intent;
    return true;
}

bool fhir_careplan_add_activity(FHIRCarePlan* self, const FHIRCarePlanActivity* activity) {
    if (!self || !activity) return false;
    
    return fhir_array_add((void***)&self->activity, &self->activity_count,
                         (void*)activity, sizeof(FHIRCarePlanActivity));
}

const char* fhir_careplan_status_to_string(FHIRCarePlanStatus status) {
    switch (status) {
        case FHIR_CAREPLAN_STATUS_DRAFT: return "draft";
        case FHIR_CAREPLAN_STATUS_ACTIVE: return "active";
        case FHIR_CAREPLAN_STATUS_ON_HOLD: return "on-hold";
        case FHIR_CAREPLAN_STATUS_REVOKED: return "revoked";
        case FHIR_CAREPLAN_STATUS_COMPLETED: return "completed";
        case FHIR_CAREPLAN_STATUS_ENTERED_IN_ERROR: return "entered-in-error";
        default: return "unknown";
    }
}

FHIRCarePlanStatus fhir_careplan_status_from_string(const char* status_str) {
    if (!status_str) return FHIR_CAREPLAN_STATUS_UNKNOWN;
    
    if (strcmp(status_str, "draft") == 0) return FHIR_CAREPLAN_STATUS_DRAFT;
    if (strcmp(status_str, "active") == 0) return FHIR_CAREPLAN_STATUS_ACTIVE;
    if (strcmp(status_str, "on-hold") == 0) return FHIR_CAREPLAN_STATUS_ON_HOLD;
    if (strcmp(status_str, "revoked") == 0) return FHIR_CAREPLAN_STATUS_REVOKED;
    if (strcmp(status_str, "completed") == 0) return FHIR_CAREPLAN_STATUS_COMPLETED;
    if (strcmp(status_str, "entered-in-error") == 0) return FHIR_CAREPLAN_STATUS_ENTERED_IN_ERROR;
    
    return FHIR_CAREPLAN_STATUS_UNKNOWN;
}

const char* fhir_careplan_intent_to_string(FHIRCarePlanIntent intent) {
    switch (intent) {
        case FHIR_CAREPLAN_INTENT_PROPOSAL: return "proposal";
        case FHIR_CAREPLAN_INTENT_PLAN: return "plan";
        case FHIR_CAREPLAN_INTENT_ORDER: return "order";
        case FHIR_CAREPLAN_INTENT_OPTION: return "option";
        case FHIR_CAREPLAN_INTENT_DIRECTIVE: return "directive";
        default: return "proposal";
    }
}

FHIRCarePlanIntent fhir_careplan_intent_from_string(const char* intent_str) {
    if (!intent_str) return FHIR_CAREPLAN_INTENT_PROPOSAL;
    
    if (strcmp(intent_str, "proposal") == 0) return FHIR_CAREPLAN_INTENT_PROPOSAL;
    if (strcmp(intent_str, "plan") == 0) return FHIR_CAREPLAN_INTENT_PLAN;
    if (strcmp(intent_str, "order") == 0) return FHIR_CAREPLAN_INTENT_ORDER;
    if (strcmp(intent_str, "option") == 0) return FHIR_CAREPLAN_INTENT_OPTION;
    if (strcmp(intent_str, "directive") == 0) return FHIR_CAREPLAN_INTENT_DIRECTIVE;
    
    return FHIR_CAREPLAN_INTENT_PROPOSAL;
}

bool fhir_careplan_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_CAREPLAN,
        .name = "CarePlan",
        .vtable = &CarePlan_vtable,
        .factory = (FHIRResourceFactory)fhir_careplan_create
    };
    
    return fhir_resource_register_type(&registration);
}