/**
 * @file fhir_practitionerrole.c
 * @brief FHIR R5 PractitionerRole resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_practitionerrole.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(PractitionerRole, practitionerrole)

/* ========================================================================== */
/* PractitionerRole Factory and Lifecycle Methods                             */
/* ========================================================================== */

FHIRPractitionerRole* fhir_practitionerrole_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRPractitionerRole* practitionerrole = fhir_calloc(1, sizeof(FHIRPractitionerRole));
    if (!practitionerrole) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&practitionerrole->base, &PractitionerRole_vtable, 
                                FHIR_RESOURCE_TYPE_PRACTITIONERROLE, id)) {
        fhir_free(practitionerrole);
        return NULL;
    }
    
    // Initialize PractitionerRole-specific defaults
    practitionerrole->active = fhir_boolean_create(true);
    
    return practitionerrole;
}

void fhir_practitionerrole_destroy(FHIRPractitionerRole* self) {
    if (!self) return;
    
    // Free PractitionerRole-specific fields
    if (self->active) fhir_boolean_destroy(self->active);
    if (self->period) fhir_period_destroy(self->period);
    if (self->practitioner) fhir_reference_destroy(self->practitioner);
    if (self->organization) fhir_reference_destroy(self->organization);
    
    // Free arrays
    fhir_array_destroy((void**)self->code, self->code_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->specialty, self->specialty_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->location, self->location_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->healthcare_service, self->healthcare_service_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->contact, self->contact_count, (FHIRDestroyFunc)fhir_extendedcontactdetail_destroy);
    fhir_array_destroy((void**)self->characteristic, self->characteristic_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->communication, self->communication_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->availability, self->availability_count, (FHIRDestroyFunc)fhir_availability_destroy);
    fhir_array_destroy((void**)self->endpoint, self->endpoint_count, (FHIRDestroyFunc)fhir_reference_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRPractitionerRole* fhir_practitionerrole_clone(const FHIRPractitionerRole* self) {
    if (!self) return NULL;
    
    FHIRPractitionerRole* clone = fhir_practitionerrole_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone PractitionerRole-specific fields
    if (self->active) {
        clone->active = fhir_boolean_clone(self->active);
    }
    if (self->period) {
        clone->period = fhir_period_clone(self->period);
    }
    if (self->practitioner) {
        clone->practitioner = fhir_reference_clone(self->practitioner);
    }
    if (self->organization) {
        clone->organization = fhir_reference_clone(self->organization);
    }
    
    // Clone arrays
    clone->code = fhir_array_clone((void**)self->code, self->code_count, 
                                  (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->code_count);
    clone->specialty = fhir_array_clone((void**)self->specialty, self->specialty_count, 
                                       (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->specialty_count);
    clone->location = fhir_array_clone((void**)self->location, self->location_count, 
                                      (FHIRCloneFunc)fhir_reference_clone, &clone->location_count);
    
    return clone;
}

/* ========================================================================== */
/* PractitionerRole Serialization Methods                                     */
/* ========================================================================== */

cJSON* fhir_practitionerrole_to_json(const FHIRPractitionerRole* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "PractitionerRole is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "PractitionerRole") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add PractitionerRole-specific fields
    if (self->active) {
        fhir_json_add_boolean(json, "active", self->active);
    }
    if (self->period) {
        fhir_json_add_period(json, "period", self->period);
    }
    if (self->practitioner) {
        fhir_json_add_reference(json, "practitioner", self->practitioner);
    }
    if (self->organization) {
        fhir_json_add_reference(json, "organization", self->organization);
    }
    
    // Add arrays
    if (self->code && self->code_count > 0) {
        fhir_json_add_codeableconcept_array(json, "code", self->code, self->code_count);
    }
    if (self->specialty && self->specialty_count > 0) {
        fhir_json_add_codeableconcept_array(json, "specialty", self->specialty, self->specialty_count);
    }
    if (self->location && self->location_count > 0) {
        fhir_json_add_reference_array(json, "location", self->location, self->location_count);
    }
    
    return json;
}

bool fhir_practitionerrole_from_json(FHIRPractitionerRole* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "PractitionerRole") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse PractitionerRole-specific fields
    const cJSON* active_json = cJSON_GetObjectItem(json, "active");
    if (active_json) {
        self->active = fhir_json_parse_boolean(active_json);
    }
    
    const cJSON* period_json = cJSON_GetObjectItem(json, "period");
    if (period_json) {
        self->period = fhir_json_parse_period(period_json);
    }
    
    const cJSON* practitioner_json = cJSON_GetObjectItem(json, "practitioner");
    if (practitioner_json) {
        self->practitioner = fhir_json_parse_reference(practitioner_json);
    }
    
    const cJSON* organization_json = cJSON_GetObjectItem(json, "organization");
    if (organization_json) {
        self->organization = fhir_json_parse_reference(organization_json);
    }
    
    // Parse arrays
    const cJSON* code_json = cJSON_GetObjectItem(json, "code");
    if (code_json && cJSON_IsArray(code_json)) {
        self->code = fhir_json_parse_codeableconcept_array(code_json, &self->code_count);
    }
    
    const cJSON* specialty_json = cJSON_GetObjectItem(json, "specialty");
    if (specialty_json && cJSON_IsArray(specialty_json)) {
        self->specialty = fhir_json_parse_codeableconcept_array(specialty_json, &self->specialty_count);
    }
    
    return true;
}

FHIRPractitionerRole* fhir_practitionerrole_parse(const char* json_string) {
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
    
    FHIRPractitionerRole* practitionerrole = fhir_practitionerrole_create(id);
    if (!practitionerrole) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_practitionerrole_from_json(practitionerrole, json)) {
        fhir_practitionerrole_destroy(practitionerrole);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return practitionerrole;
}

/* ========================================================================== */
/* PractitionerRole Validation Methods                                        */
/* ========================================================================== */

bool fhir_practitionerrole_validate(const FHIRPractitionerRole* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("PractitionerRole", self->base.id)) {
        return false;
    }
    
    // Validate required fields
    if (!self->practitioner) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "practitioner");
        return false;
    }
    
    if (!self->organization) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "organization");
        return false;
    }
    
    return true;
}

/* ========================================================================== */
/* PractitionerRole-Specific Methods                                          */
/* ========================================================================== */

bool fhir_practitionerrole_is_active(const FHIRPractitionerRole* self) {
    if (!self || !self->active) return false;
    return self->active->value;
}

const char* fhir_practitionerrole_get_display_name(const FHIRPractitionerRole* self) {
    if (!self) return NULL;
    
    // Return practitioner reference display if available
    if (self->practitioner && self->practitioner->display) {
        return self->practitioner->display->value;
    }
    
    return "PractitionerRole";
}

bool fhir_practitionerrole_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_PRACTITIONERROLE,
        .name = "PractitionerRole",
        .vtable = &PractitionerRole_vtable,
        .factory = (FHIRResourceFactory)fhir_practitionerrole_create
    };
    
    return fhir_resource_register_type(&registration);
}