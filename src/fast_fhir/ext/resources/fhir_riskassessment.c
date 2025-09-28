/**
 * @file fhir_riskassessment.c
 * @brief FHIR R5 RiskAssessment resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_riskassessment.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(RiskAssessment, riskassessment)

/* ========================================================================== */
/* RiskAssessment Sub-structure Methods                                      */
/* ========================================================================== */

FHIRRiskAssessmentPrediction* fhir_riskassessment_prediction_create(void) {
    FHIRRiskAssessmentPrediction* prediction = fhir_calloc(1, sizeof(FHIRRiskAssessmentPrediction));
    if (!prediction) return NULL;
    
    fhir_element_init(&prediction->base);
    return prediction;
}

void fhir_riskassessment_prediction_destroy(FHIRRiskAssessmentPrediction* self) {
    if (!self) return;
    
    if (self->outcome) fhir_codeableconcept_destroy(self->outcome);
    if (self->probability_decimal) fhir_decimal_destroy(self->probability_decimal);
    if (self->probability_range) fhir_range_destroy(self->probability_range);
    if (self->qualitative_risk) fhir_codeableconcept_destroy(self->qualitative_risk);
    if (self->relative_risk) fhir_decimal_destroy(self->relative_risk);
    if (self->when_period) fhir_period_destroy(self->when_period);
    if (self->when_range) fhir_range_destroy(self->when_range);
    if (self->rationale) fhir_string_destroy(self->rationale);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

/* ========================================================================== */
/* RiskAssessment Factory and Lifecycle Methods                             */
/* ========================================================================== */

FHIRRiskAssessment* fhir_riskassessment_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRRiskAssessment* riskassessment = fhir_calloc(1, sizeof(FHIRRiskAssessment));
    if (!riskassessment) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&riskassessment->base, &RiskAssessment_vtable, 
                                FHIR_RESOURCE_TYPE_RISKASSESSMENT, id)) {
        fhir_free(riskassessment);
        return NULL;
    }
    
    // Initialize RiskAssessment-specific defaults
    riskassessment->status = FHIR_RISKASSESSMENT_STATUS_REGISTERED;
    
    return riskassessment;
}

void fhir_riskassessment_destroy(FHIRRiskAssessment* self) {
    if (!self) return;
    
    // Free RiskAssessment-specific fields
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    if (self->based_on) fhir_reference_destroy(self->based_on);
    if (self->parent) fhir_reference_destroy(self->parent);
    if (self->method) fhir_codeableconcept_destroy(self->method);
    if (self->code) fhir_codeableconcept_destroy(self->code);
    if (self->subject) fhir_reference_destroy(self->subject);
    if (self->encounter) fhir_reference_destroy(self->encounter);
    if (self->occurrence_date_time) fhir_datetime_destroy(self->occurrence_date_time);
    if (self->occurrence_period) fhir_period_destroy(self->occurrence_period);
    if (self->condition) fhir_reference_destroy(self->condition);
    if (self->performer) fhir_reference_destroy(self->performer);
    fhir_array_destroy((void**)self->reason_code, self->reason_code_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->reason_reference, self->reason_reference_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->basis, self->basis_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->prediction, self->prediction_count, (FHIRDestroyFunc)fhir_riskassessment_prediction_destroy);
    if (self->mitigation) fhir_string_destroy(self->mitigation);
    fhir_array_destroy((void**)self->note, self->note_count, (FHIRDestroyFunc)fhir_annotation_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRRiskAssessment* fhir_riskassessment_clone(const FHIRRiskAssessment* self) {
    if (!self) return NULL;
    
    FHIRRiskAssessment* clone = fhir_riskassessment_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone RiskAssessment-specific fields
    clone->status = self->status;
    
    clone->identifier = fhir_array_clone((void**)self->identifier, self->identifier_count, 
                                        (FHIRCloneFunc)fhir_identifier_clone, &clone->identifier_count);
    
    if (self->based_on) {
        clone->based_on = fhir_reference_clone(self->based_on);
    }
    
    if (self->parent) {
        clone->parent = fhir_reference_clone(self->parent);
    }
    
    if (self->method) {
        clone->method = fhir_codeableconcept_clone(self->method);
    }
    
    if (self->code) {
        clone->code = fhir_codeableconcept_clone(self->code);
    }
    
    if (self->subject) {
        clone->subject = fhir_reference_clone(self->subject);
    }
    
    if (self->encounter) {
        clone->encounter = fhir_reference_clone(self->encounter);
    }
    
    if (self->occurrence_date_time) {
        clone->occurrence_date_time = fhir_datetime_clone(self->occurrence_date_time);
    }
    
    if (self->occurrence_period) {
        clone->occurrence_period = fhir_period_clone(self->occurrence_period);
    }
    
    if (self->condition) {
        clone->condition = fhir_reference_clone(self->condition);
    }
    
    if (self->performer) {
        clone->performer = fhir_reference_clone(self->performer);
    }
    
    clone->reason_code = fhir_array_clone((void**)self->reason_code, self->reason_code_count, 
                                         (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->reason_code_count);
    
    clone->reason_reference = fhir_array_clone((void**)self->reason_reference, self->reason_reference_count, 
                                              (FHIRCloneFunc)fhir_reference_clone, &clone->reason_reference_count);
    
    clone->basis = fhir_array_clone((void**)self->basis, self->basis_count, 
                                   (FHIRCloneFunc)fhir_reference_clone, &clone->basis_count);
    
    if (self->mitigation) {
        clone->mitigation = fhir_string_clone(self->mitigation);
    }
    
    clone->note = fhir_array_clone((void**)self->note, self->note_count, 
                                  (FHIRCloneFunc)fhir_annotation_clone, &clone->note_count);
    
    return clone;
}

/* ========================================================================== */
/* RiskAssessment Serialization Methods                                      */
/* ========================================================================== */

cJSON* fhir_riskassessment_to_json(const FHIRRiskAssessment* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "RiskAssessment is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "RiskAssessment") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add status
    const char* status_str = fhir_riskassessment_status_to_string(self->status);
    fhir_json_add_string(json, "status", status_str);
    
    // Add RiskAssessment-specific fields
    if (self->identifier && self->identifier_count > 0) {
        fhir_json_add_identifier_array(json, "identifier", self->identifier, self->identifier_count);
    }
    
    if (self->based_on) {
        fhir_json_add_reference(json, "basedOn", self->based_on);
    }
    
    if (self->parent) {
        fhir_json_add_reference(json, "parent", self->parent);
    }
    
    if (self->method) {
        fhir_json_add_codeableconcept(json, "method", self->method);
    }
    
    if (self->code) {
        fhir_json_add_codeableconcept(json, "code", self->code);
    }
    
    if (self->subject) {
        fhir_json_add_reference(json, "subject", self->subject);
    }
    
    if (self->encounter) {
        fhir_json_add_reference(json, "encounter", self->encounter);
    }
    
    // Add occurrence (choice type)
    if (self->occurrence_date_time) {
        fhir_json_add_datetime(json, "occurrenceDateTime", self->occurrence_date_time);
    } else if (self->occurrence_period) {
        fhir_json_add_period(json, "occurrencePeriod", self->occurrence_period);
    }
    
    if (self->condition) {
        fhir_json_add_reference(json, "condition", self->condition);
    }
    
    if (self->performer) {
        fhir_json_add_reference(json, "performer", self->performer);
    }
    
    if (self->reason_code && self->reason_code_count > 0) {
        fhir_json_add_codeableconcept_array(json, "reasonCode", self->reason_code, self->reason_code_count);
    }
    
    if (self->reason_reference && self->reason_reference_count > 0) {
        fhir_json_add_reference_array(json, "reasonReference", self->reason_reference, self->reason_reference_count);
    }
    
    if (self->basis && self->basis_count > 0) {
        fhir_json_add_reference_array(json, "basis", self->basis, self->basis_count);
    }
    
    if (self->mitigation) {
        fhir_json_add_string_value(json, "mitigation", self->mitigation);
    }
    
    if (self->note && self->note_count > 0) {
        fhir_json_add_annotation_array(json, "note", self->note, self->note_count);
    }
    
    return json;
}

bool fhir_riskassessment_from_json(FHIRRiskAssessment* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "RiskAssessment") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse status
    const char* status_str = fhir_json_get_string(json, "status");
    if (status_str) {
        self->status = fhir_riskassessment_status_from_string(status_str);
    }
    
    // Parse RiskAssessment-specific fields
    const cJSON* identifier_json = cJSON_GetObjectItem(json, "identifier");
    if (identifier_json && cJSON_IsArray(identifier_json)) {
        self->identifier = fhir_json_parse_identifier_array(identifier_json, &self->identifier_count);
    }
    
    const cJSON* based_on_json = cJSON_GetObjectItem(json, "basedOn");
    if (based_on_json) {
        self->based_on = fhir_json_parse_reference(based_on_json);
    }
    
    const cJSON* parent_json = cJSON_GetObjectItem(json, "parent");
    if (parent_json) {
        self->parent = fhir_json_parse_reference(parent_json);
    }
    
    const cJSON* method_json = cJSON_GetObjectItem(json, "method");
    if (method_json) {
        self->method = fhir_json_parse_codeableconcept(method_json);
    }
    
    const cJSON* code_json = cJSON_GetObjectItem(json, "code");
    if (code_json) {
        self->code = fhir_json_parse_codeableconcept(code_json);
    }
    
    const cJSON* subject_json = cJSON_GetObjectItem(json, "subject");
    if (subject_json) {
        self->subject = fhir_json_parse_reference(subject_json);
    }
    
    const cJSON* encounter_json = cJSON_GetObjectItem(json, "encounter");
    if (encounter_json) {
        self->encounter = fhir_json_parse_reference(encounter_json);
    }
    
    // Parse occurrence (choice type)
    const cJSON* occurrence_datetime_json = cJSON_GetObjectItem(json, "occurrenceDateTime");
    if (occurrence_datetime_json) {
        self->occurrence_date_time = fhir_json_parse_datetime(occurrence_datetime_json);
    }
    
    const cJSON* occurrence_period_json = cJSON_GetObjectItem(json, "occurrencePeriod");
    if (occurrence_period_json) {
        self->occurrence_period = fhir_json_parse_period(occurrence_period_json);
    }
    
    const cJSON* condition_json = cJSON_GetObjectItem(json, "condition");
    if (condition_json) {
        self->condition = fhir_json_parse_reference(condition_json);
    }
    
    const cJSON* performer_json = cJSON_GetObjectItem(json, "performer");
    if (performer_json) {
        self->performer = fhir_json_parse_reference(performer_json);
    }
    
    const cJSON* reason_code_json = cJSON_GetObjectItem(json, "reasonCode");
    if (reason_code_json && cJSON_IsArray(reason_code_json)) {
        self->reason_code = fhir_json_parse_codeableconcept_array(reason_code_json, &self->reason_code_count);
    }
    
    const cJSON* reason_reference_json = cJSON_GetObjectItem(json, "reasonReference");
    if (reason_reference_json && cJSON_IsArray(reason_reference_json)) {
        self->reason_reference = fhir_json_parse_reference_array(reason_reference_json, &self->reason_reference_count);
    }
    
    const cJSON* basis_json = cJSON_GetObjectItem(json, "basis");
    if (basis_json && cJSON_IsArray(basis_json)) {
        self->basis = fhir_json_parse_reference_array(basis_json, &self->basis_count);
    }
    
    const cJSON* mitigation_json = cJSON_GetObjectItem(json, "mitigation");
    if (mitigation_json) {
        self->mitigation = fhir_json_parse_string(mitigation_json);
    }
    
    const cJSON* note_json = cJSON_GetObjectItem(json, "note");
    if (note_json && cJSON_IsArray(note_json)) {
        self->note = fhir_json_parse_annotation_array(note_json, &self->note_count);
    }
    
    return true;
}

FHIRRiskAssessment* fhir_riskassessment_parse(const char* json_string) {
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
    
    FHIRRiskAssessment* riskassessment = fhir_riskassessment_create(id);
    if (!riskassessment) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_riskassessment_from_json(riskassessment, json)) {
        fhir_riskassessment_destroy(riskassessment);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return riskassessment;
}

/* ========================================================================== */
/* RiskAssessment Validation Methods                                         */
/* ========================================================================== */

bool fhir_riskassessment_validate(const FHIRRiskAssessment* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("RiskAssessment", self->base.id)) {
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
/* RiskAssessment-Specific Methods                                           */
/* ========================================================================== */

bool fhir_riskassessment_is_active(const FHIRRiskAssessment* self) {
    if (!self) return false;
    return self->status == FHIR_RISKASSESSMENT_STATUS_FINAL ||
           self->status == FHIR_RISKASSESSMENT_STATUS_AMENDED ||
           self->status == FHIR_RISKASSESSMENT_STATUS_CORRECTED;
}

const char* fhir_riskassessment_get_display_name(const FHIRRiskAssessment* self) {
    if (!self) return NULL;
    
    // Return code display if available
    if (self->code && self->code->text && self->code->text->value) {
        return self->code->text->value;
    }
    
    return "RiskAssessment";
}

bool fhir_riskassessment_set_status(FHIRRiskAssessment* self, FHIRRiskAssessmentStatus status) {
    if (!self) return false;
    
    self->status = status;
    return true;
}

bool fhir_riskassessment_add_prediction(FHIRRiskAssessment* self, const FHIRRiskAssessmentPrediction* prediction) {
    if (!self || !prediction) return false;
    
    return fhir_array_add((void***)&self->prediction, &self->prediction_count,
                         (void*)prediction, sizeof(FHIRRiskAssessmentPrediction));
}

FHIRRiskAssessmentPrediction* fhir_riskassessment_get_highest_risk_prediction(const FHIRRiskAssessment* self) {
    if (!self || !self->prediction || self->prediction_count == 0) return NULL;
    
    FHIRRiskAssessmentPrediction* highest = NULL;
    double highest_risk = 0.0;
    
    for (size_t i = 0; i < self->prediction_count; i++) {
        FHIRRiskAssessmentPrediction* pred = self->prediction[i];
        if (!pred) continue;
        
        double risk = 0.0;
        if (pred->probability_decimal && pred->probability_decimal->value) {
            risk = pred->probability_decimal->value;
        } else if (pred->probability_range && pred->probability_range->high && 
                   pred->probability_range->high->value) {
            risk = pred->probability_range->high->value->value;
        }
        
        if (risk > highest_risk) {
            highest_risk = risk;
            highest = pred;
        }
    }
    
    return highest;
}

bool fhir_riskassessment_is_high_risk(const FHIRRiskAssessment* self, double threshold) {
    if (!self || !self->prediction || self->prediction_count == 0) return false;
    
    for (size_t i = 0; i < self->prediction_count; i++) {
        FHIRRiskAssessmentPrediction* pred = self->prediction[i];
        if (!pred) continue;
        
        double risk = 0.0;
        if (pred->probability_decimal && pred->probability_decimal->value) {
            risk = pred->probability_decimal->value;
        } else if (pred->probability_range && pred->probability_range->high && 
                   pred->probability_range->high->value) {
            risk = pred->probability_range->high->value->value;
        }
        
        if (risk >= threshold) {
            return true;
        }
    }
    
    return false;
}

const char* fhir_riskassessment_status_to_string(FHIRRiskAssessmentStatus status) {
    switch (status) {
        case FHIR_RISKASSESSMENT_STATUS_REGISTERED: return "registered";
        case FHIR_RISKASSESSMENT_STATUS_PRELIMINARY: return "preliminary";
        case FHIR_RISKASSESSMENT_STATUS_FINAL: return "final";
        case FHIR_RISKASSESSMENT_STATUS_AMENDED: return "amended";
        case FHIR_RISKASSESSMENT_STATUS_CORRECTED: return "corrected";
        case FHIR_RISKASSESSMENT_STATUS_CANCELLED: return "cancelled";
        case FHIR_RISKASSESSMENT_STATUS_ENTERED_IN_ERROR: return "entered-in-error";
        default: return "unknown";
    }
}

FHIRRiskAssessmentStatus fhir_riskassessment_status_from_string(const char* status_str) {
    if (!status_str) return FHIR_RISKASSESSMENT_STATUS_UNKNOWN;
    
    if (strcmp(status_str, "registered") == 0) return FHIR_RISKASSESSMENT_STATUS_REGISTERED;
    if (strcmp(status_str, "preliminary") == 0) return FHIR_RISKASSESSMENT_STATUS_PRELIMINARY;
    if (strcmp(status_str, "final") == 0) return FHIR_RISKASSESSMENT_STATUS_FINAL;
    if (strcmp(status_str, "amended") == 0) return FHIR_RISKASSESSMENT_STATUS_AMENDED;
    if (strcmp(status_str, "corrected") == 0) return FHIR_RISKASSESSMENT_STATUS_CORRECTED;
    if (strcmp(status_str, "cancelled") == 0) return FHIR_RISKASSESSMENT_STATUS_CANCELLED;
    if (strcmp(status_str, "entered-in-error") == 0) return FHIR_RISKASSESSMENT_STATUS_ENTERED_IN_ERROR;
    
    return FHIR_RISKASSESSMENT_STATUS_UNKNOWN;
}

bool fhir_riskassessment_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_RISKASSESSMENT,
        .name = "RiskAssessment",
        .vtable = &RiskAssessment_vtable,
        .factory = (FHIRResourceFactory)fhir_riskassessment_create
    };
    
    return fhir_resource_register_type(&registration);
}