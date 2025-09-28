/**
 * @file fhir_observation.c
 * @brief FHIR R5 Observation resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_observation.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Observation, observation)

/* ========================================================================== */
/* Observation Sub-structure Methods                                         */
/* ========================================================================== */

FHIRObservationComponent* fhir_observation_component_create(void) {
    FHIRObservationComponent* component = fhir_calloc(1, sizeof(FHIRObservationComponent));
    if (!component) return NULL;
    
    fhir_element_init(&component->base);
    return component;
}

void fhir_observation_component_destroy(FHIRObservationComponent* self) {
    if (!self) return;
    
    if (self->code) fhir_codeableconcept_destroy(self->code);
    
    // Free value choice type fields
    if (self->value_quantity) fhir_quantity_destroy(self->value_quantity);
    if (self->value_codeable_concept) fhir_codeableconcept_destroy(self->value_codeable_concept);
    if (self->value_string) fhir_string_destroy(self->value_string);
    if (self->value_boolean) fhir_boolean_destroy(self->value_boolean);
    if (self->value_integer) fhir_integer_destroy(self->value_integer);
    if (self->value_range) fhir_range_destroy(self->value_range);
    if (self->value_ratio) fhir_ratio_destroy(self->value_ratio);
    if (self->value_sampled_data) fhir_sampleddata_destroy(self->value_sampled_data);
    if (self->value_time) fhir_time_destroy(self->value_time);
    if (self->value_date_time) fhir_datetime_destroy(self->value_date_time);
    if (self->value_period) fhir_period_destroy(self->value_period);
    if (self->value_attachment) fhir_attachment_destroy(self->value_attachment);
    if (self->value_reference) fhir_reference_destroy(self->value_reference);
    
    if (self->data_absent_reason) fhir_codeableconcept_destroy(self->data_absent_reason);
    fhir_array_destroy((void**)self->interpretation, self->interpretation_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->reference_range, self->reference_range_count, (FHIRDestroyFunc)fhir_observation_reference_range_destroy);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIRObservationReferenceRange* fhir_observation_reference_range_create(void) {
    FHIRObservationReferenceRange* range = fhir_calloc(1, sizeof(FHIRObservationReferenceRange));
    if (!range) return NULL;
    
    fhir_element_init(&range->base);
    return range;
}

void fhir_observation_reference_range_destroy(FHIRObservationReferenceRange* self) {
    if (!self) return;
    
    if (self->low) fhir_quantity_destroy(self->low);
    if (self->high) fhir_quantity_destroy(self->high);
    if (self->normal_value) fhir_codeableconcept_destroy(self->normal_value);
    if (self->type) fhir_codeableconcept_destroy(self->type);
    fhir_array_destroy((void**)self->applies_to, self->applies_to_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->age) fhir_range_destroy(self->age);
    if (self->text) fhir_string_destroy(self->text);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

/* ========================================================================== */
/* Observation Factory and Lifecycle Methods                                 */
/* ========================================================================== */

FHIRObservation* fhir_observation_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRObservation* observation = fhir_calloc(1, sizeof(FHIRObservation));
    if (!observation) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&observation->base, &Observation_vtable, 
                                FHIR_RESOURCE_TYPE_OBSERVATION, id)) {
        fhir_free(observation);
        return NULL;
    }
    
    // Initialize Observation-specific defaults
    observation->status = FHIR_OBSERVATION_STATUS_REGISTERED;
    
    return observation;
}

void fhir_observation_destroy(FHIRObservation* self) {
    if (!self) return;
    
    // Free Observation-specific fields
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    fhir_array_destroy((void**)self->instantiates_canonical, self->instantiates_canonical_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->instantiates_reference, self->instantiates_reference_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->based_on, self->based_on_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->triggered_by, self->triggered_by_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->part_of, self->part_of_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->category, self->category_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    if (self->code) fhir_codeableconcept_destroy(self->code);
    if (self->subject) fhir_reference_destroy(self->subject);
    fhir_array_destroy((void**)self->focus, self->focus_count, (FHIRDestroyFunc)fhir_reference_destroy);
    if (self->encounter) fhir_reference_destroy(self->encounter);
    
    // Free effective choice type fields
    if (self->effective_date_time) fhir_datetime_destroy(self->effective_date_time);
    if (self->effective_period) fhir_period_destroy(self->effective_period);
    if (self->effective_timing) fhir_timing_destroy(self->effective_timing);
    if (self->effective_instant) fhir_instant_destroy(self->effective_instant);
    
    if (self->issued) fhir_instant_destroy(self->issued);
    fhir_array_destroy((void**)self->performer, self->performer_count, (FHIRDestroyFunc)fhir_reference_destroy);
    
    // Free value choice type fields
    if (self->value_quantity) fhir_quantity_destroy(self->value_quantity);
    if (self->value_codeable_concept) fhir_codeableconcept_destroy(self->value_codeable_concept);
    if (self->value_string) fhir_string_destroy(self->value_string);
    if (self->value_boolean) fhir_boolean_destroy(self->value_boolean);
    if (self->value_integer) fhir_integer_destroy(self->value_integer);
    if (self->value_range) fhir_range_destroy(self->value_range);
    if (self->value_ratio) fhir_ratio_destroy(self->value_ratio);
    if (self->value_sampled_data) fhir_sampleddata_destroy(self->value_sampled_data);
    if (self->value_time) fhir_time_destroy(self->value_time);
    if (self->value_date_time) fhir_datetime_destroy(self->value_date_time);
    if (self->value_period) fhir_period_destroy(self->value_period);
    if (self->value_attachment) fhir_attachment_destroy(self->value_attachment);
    if (self->value_reference) fhir_reference_destroy(self->value_reference);
    
    if (self->data_absent_reason) fhir_codeableconcept_destroy(self->data_absent_reason);
    fhir_array_destroy((void**)self->interpretation, self->interpretation_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->note, self->note_count, (FHIRDestroyFunc)fhir_annotation_destroy);
    if (self->body_site) fhir_codeableconcept_destroy(self->body_site);
    if (self->method) fhir_codeableconcept_destroy(self->method);
    if (self->specimen) fhir_reference_destroy(self->specimen);
    if (self->device) fhir_reference_destroy(self->device);
    fhir_array_destroy((void**)self->reference_range, self->reference_range_count, (FHIRDestroyFunc)fhir_observation_reference_range_destroy);
    fhir_array_destroy((void**)self->has_member, self->has_member_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->derived_from, self->derived_from_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->component, self->component_count, (FHIRDestroyFunc)fhir_observation_component_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRObservation* fhir_observation_clone(const FHIRObservation* self) {
    if (!self) return NULL;
    
    FHIRObservation* clone = fhir_observation_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone Observation-specific fields
    clone->identifier = fhir_array_clone((void**)self->identifier, self->identifier_count, 
                                        (FHIRCloneFunc)fhir_identifier_clone, &clone->identifier_count);
    
    clone->status = self->status;
    
    clone->category = fhir_array_clone((void**)self->category, self->category_count, 
                                      (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->category_count);
    
    if (self->code) {
        clone->code = fhir_codeableconcept_clone(self->code);
    }
    
    if (self->subject) {
        clone->subject = fhir_reference_clone(self->subject);
    }
    
    if (self->encounter) {
        clone->encounter = fhir_reference_clone(self->encounter);
    }
    
    // Clone effective choice type (simplified - only datetime for now)
    if (self->effective_date_time) {
        clone->effective_date_time = fhir_datetime_clone(self->effective_date_time);
    }
    
    // Clone value choice type (simplified - only quantity for now)
    if (self->value_quantity) {
        clone->value_quantity = fhir_quantity_clone(self->value_quantity);
    }
    
    return clone;
}

/* ========================================================================== */
/* Observation Serialization Methods                                         */
/* ========================================================================== */

cJSON* fhir_observation_to_json(const FHIRObservation* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Observation is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "Observation") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add status
    const char* status_str = fhir_observation_status_to_string(self->status);
    fhir_json_add_string(json, "status", status_str);
    
    // Add code (required)
    if (self->code) {
        fhir_json_add_codeableconcept(json, "code", self->code);
    }
    
    // Add subject
    if (self->subject) {
        fhir_json_add_reference(json, "subject", self->subject);
    }
    
    // Add encounter
    if (self->encounter) {
        fhir_json_add_reference(json, "encounter", self->encounter);
    }
    
    // Add effective datetime (simplified)
    if (self->effective_date_time) {
        fhir_json_add_datetime(json, "effectiveDateTime", self->effective_date_time);
    }
    
    // Add value (simplified - only quantity for now)
    if (self->value_quantity) {
        fhir_json_add_quantity(json, "valueQuantity", self->value_quantity);
    } else if (self->value_string) {
        fhir_json_add_string_value(json, "valueString", self->value_string);
    } else if (self->value_boolean) {
        fhir_json_add_boolean(json, "valueBoolean", self->value_boolean);
    }
    
    // Add arrays
    if (self->category && self->category_count > 0) {
        fhir_json_add_codeableconcept_array(json, "category", self->category, self->category_count);
    }
    
    if (self->performer && self->performer_count > 0) {
        fhir_json_add_reference_array(json, "performer", self->performer, self->performer_count);
    }
    
    return json;
}

bool fhir_observation_from_json(FHIRObservation* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "Observation") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse status
    const char* status_str = fhir_json_get_string(json, "status");
    if (status_str) {
        self->status = fhir_observation_status_from_string(status_str);
    }
    
    // Parse code (required)
    const cJSON* code_json = cJSON_GetObjectItem(json, "code");
    if (code_json) {
        self->code = fhir_json_parse_codeableconcept(code_json);
    }
    
    // Parse subject
    const cJSON* subject_json = cJSON_GetObjectItem(json, "subject");
    if (subject_json) {
        self->subject = fhir_json_parse_reference(subject_json);
    }
    
    // Parse encounter
    const cJSON* encounter_json = cJSON_GetObjectItem(json, "encounter");
    if (encounter_json) {
        self->encounter = fhir_json_parse_reference(encounter_json);
    }
    
    // Parse effective datetime
    const cJSON* effective_json = cJSON_GetObjectItem(json, "effectiveDateTime");
    if (effective_json) {
        self->effective_date_time = fhir_json_parse_datetime(effective_json);
    }
    
    // Parse value (simplified)
    const cJSON* value_quantity_json = cJSON_GetObjectItem(json, "valueQuantity");
    if (value_quantity_json) {
        self->value_quantity = fhir_json_parse_quantity(value_quantity_json);
    }
    
    const cJSON* value_string_json = cJSON_GetObjectItem(json, "valueString");
    if (value_string_json) {
        self->value_string = fhir_json_parse_string(value_string_json);
    }
    
    const cJSON* value_boolean_json = cJSON_GetObjectItem(json, "valueBoolean");
    if (value_boolean_json) {
        self->value_boolean = fhir_json_parse_boolean(value_boolean_json);
    }
    
    // Parse arrays
    const cJSON* category_json = cJSON_GetObjectItem(json, "category");
    if (category_json && cJSON_IsArray(category_json)) {
        self->category = fhir_json_parse_codeableconcept_array(category_json, &self->category_count);
    }
    
    const cJSON* performer_json = cJSON_GetObjectItem(json, "performer");
    if (performer_json && cJSON_IsArray(performer_json)) {
        self->performer = fhir_json_parse_reference_array(performer_json, &self->performer_count);
    }
    
    return true;
}

FHIRObservation* fhir_observation_parse(const char* json_string) {
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
    
    FHIRObservation* observation = fhir_observation_create(id);
    if (!observation) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_observation_from_json(observation, json)) {
        fhir_observation_destroy(observation);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return observation;
}

/* ========================================================================== */
/* Observation Validation Methods                                            */
/* ========================================================================== */

bool fhir_observation_validate(const FHIRObservation* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("Observation", self->base.id)) {
        return false;
    }
    
    // Validate required fields
    if (!self->code) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "code");
        return false;
    }
    
    return true;
}

/* ========================================================================== */
/* Observation-Specific Methods                                              */
/* ========================================================================== */

bool fhir_observation_is_active(const FHIRObservation* self) {
    if (!self) return false;
    return self->status == FHIR_OBSERVATION_STATUS_FINAL ||
           self->status == FHIR_OBSERVATION_STATUS_AMENDED ||
           self->status == FHIR_OBSERVATION_STATUS_CORRECTED;
}

const char* fhir_observation_get_display_name(const FHIRObservation* self) {
    if (!self) return NULL;
    
    // Return code display if available
    if (self->code && self->code->text && self->code->text->value) {
        return self->code->text->value;
    }
    
    return "Observation";
}

bool fhir_observation_has_value(const FHIRObservation* self) {
    if (!self) return false;
    
    return self->value_quantity || self->value_codeable_concept || 
           self->value_string || self->value_boolean || self->value_integer ||
           self->value_range || self->value_ratio || self->value_sampled_data ||
           self->value_time || self->value_date_time || self->value_period ||
           self->value_attachment || self->value_reference;
}

char* fhir_observation_get_value_string(const FHIRObservation* self) {
    if (!self) return NULL;
    
    // Simplified implementation - return string representation of value
    if (self->value_string && self->value_string->value) {
        return fhir_strdup(self->value_string->value);
    }
    
    if (self->value_quantity && self->value_quantity->value) {
        char* result = fhir_malloc(64);
        if (result) {
            snprintf(result, 64, "%.2f", self->value_quantity->value->value);
        }
        return result;
    }
    
    if (self->value_boolean) {
        return fhir_strdup(self->value_boolean->value ? "true" : "false");
    }
    
    return NULL;
}

bool fhir_observation_set_status(FHIRObservation* self, FHIRObservationStatus status) {
    if (!self) return false;
    
    self->status = status;
    return true;
}

const char* fhir_observation_status_to_string(FHIRObservationStatus status) {
    switch (status) {
        case FHIR_OBSERVATION_STATUS_REGISTERED: return "registered";
        case FHIR_OBSERVATION_STATUS_PRELIMINARY: return "preliminary";
        case FHIR_OBSERVATION_STATUS_FINAL: return "final";
        case FHIR_OBSERVATION_STATUS_AMENDED: return "amended";
        case FHIR_OBSERVATION_STATUS_CORRECTED: return "corrected";
        case FHIR_OBSERVATION_STATUS_CANCELLED: return "cancelled";
        case FHIR_OBSERVATION_STATUS_ENTERED_IN_ERROR: return "entered-in-error";
        default: return "unknown";
    }
}

FHIRObservationStatus fhir_observation_status_from_string(const char* status_str) {
    if (!status_str) return FHIR_OBSERVATION_STATUS_UNKNOWN;
    
    if (strcmp(status_str, "registered") == 0) return FHIR_OBSERVATION_STATUS_REGISTERED;
    if (strcmp(status_str, "preliminary") == 0) return FHIR_OBSERVATION_STATUS_PRELIMINARY;
    if (strcmp(status_str, "final") == 0) return FHIR_OBSERVATION_STATUS_FINAL;
    if (strcmp(status_str, "amended") == 0) return FHIR_OBSERVATION_STATUS_AMENDED;
    if (strcmp(status_str, "corrected") == 0) return FHIR_OBSERVATION_STATUS_CORRECTED;
    if (strcmp(status_str, "cancelled") == 0) return FHIR_OBSERVATION_STATUS_CANCELLED;
    if (strcmp(status_str, "entered-in-error") == 0) return FHIR_OBSERVATION_STATUS_ENTERED_IN_ERROR;
    
    return FHIR_OBSERVATION_STATUS_UNKNOWN;
}

bool fhir_observation_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_OBSERVATION,
        .name = "Observation",
        .vtable = &Observation_vtable,
        .factory = (FHIRResourceFactory)fhir_observation_create
    };
    
    return fhir_resource_register_type(&registration);
}