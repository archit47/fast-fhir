/**
 * @file fhir_practitioner.c
 * @brief FHIR R5 Practitioner resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_practitioner.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Practitioner, practitioner)

/* ========================================================================== */
/* Practitioner Sub-structure Methods                                        */
/* ========================================================================== */

FHIRPractitionerQualification* fhir_practitioner_qualification_create(void) {
    FHIRPractitionerQualification* qual = fhir_calloc(1, sizeof(FHIRPractitionerQualification));
    if (!qual) return NULL;
    
    fhir_element_init(&qual->base);
    return qual;
}

void fhir_practitioner_qualification_destroy(FHIRPractitionerQualification* self) {
    if (!self) return;
    
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    if (self->code) fhir_codeableconcept_destroy(self->code);
    if (self->period) fhir_period_destroy(self->period);
    if (self->issuer) fhir_reference_destroy(self->issuer);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

FHIRPractitionerCommunication* fhir_practitioner_communication_create(void) {
    FHIRPractitionerCommunication* comm = fhir_calloc(1, sizeof(FHIRPractitionerCommunication));
    if (!comm) return NULL;
    
    fhir_element_init(&comm->base);
    return comm;
}

void fhir_practitioner_communication_destroy(FHIRPractitionerCommunication* self) {
    if (!self) return;
    
    if (self->language) fhir_codeableconcept_destroy(self->language);
    if (self->preferred) fhir_boolean_destroy(self->preferred);
    
    fhir_element_cleanup(&self->base);
    fhir_free(self);
}

/* ========================================================================== */
/* Practitioner Factory and Lifecycle Methods                               */
/* ========================================================================== */

FHIRPractitioner* fhir_practitioner_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRPractitioner* practitioner = fhir_calloc(1, sizeof(FHIRPractitioner));
    if (!practitioner) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&practitioner->base, &Practitioner_vtable, 
                                FHIR_RESOURCE_TYPE_PRACTITIONER, id)) {
        fhir_free(practitioner);
        return NULL;
    }
    
    // Initialize Practitioner-specific defaults
    practitioner->active = fhir_boolean_create(true);
    practitioner->gender = FHIR_PRACTITIONER_GENDER_UNKNOWN;
    
    return practitioner;
}

void fhir_practitioner_destroy(FHIRPractitioner* self) {
    if (!self) return;
    
    // Free Practitioner-specific fields
    fhir_array_destroy((void**)self->identifier, self->identifier_count, (FHIRDestroyFunc)fhir_identifier_destroy);
    if (self->active) fhir_boolean_destroy(self->active);
    fhir_array_destroy((void**)self->name, self->name_count, (FHIRDestroyFunc)fhir_humanname_destroy);
    fhir_array_destroy((void**)self->telecom, self->telecom_count, (FHIRDestroyFunc)fhir_contactpoint_destroy);
    if (self->birth_date) fhir_date_destroy(self->birth_date);
    if (self->deceased_boolean) fhir_boolean_destroy(self->deceased_boolean);
    if (self->deceased_date_time) fhir_datetime_destroy(self->deceased_date_time);
    fhir_array_destroy((void**)self->address, self->address_count, (FHIRDestroyFunc)fhir_address_destroy);
    fhir_array_destroy((void**)self->photo, self->photo_count, (FHIRDestroyFunc)fhir_attachment_destroy);
    fhir_array_destroy((void**)self->qualification, self->qualification_count, (FHIRDestroyFunc)fhir_practitioner_qualification_destroy);
    fhir_array_destroy((void**)self->communication, self->communication_count, (FHIRDestroyFunc)fhir_practitioner_communication_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRPractitioner* fhir_practitioner_clone(const FHIRPractitioner* self) {
    if (!self) return NULL;
    
    FHIRPractitioner* clone = fhir_practitioner_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone Practitioner-specific fields
    clone->identifier = fhir_array_clone((void**)self->identifier, self->identifier_count, 
                                        (FHIRCloneFunc)fhir_identifier_clone, &clone->identifier_count);
    
    if (self->active) {
        clone->active = fhir_boolean_clone(self->active);
    }
    
    clone->name = fhir_array_clone((void**)self->name, self->name_count, 
                                  (FHIRCloneFunc)fhir_humanname_clone, &clone->name_count);
    
    clone->telecom = fhir_array_clone((void**)self->telecom, self->telecom_count, 
                                     (FHIRCloneFunc)fhir_contactpoint_clone, &clone->telecom_count);
    
    clone->gender = self->gender;
    
    if (self->birth_date) {
        clone->birth_date = fhir_date_clone(self->birth_date);
    }
    
    if (self->deceased_boolean) {
        clone->deceased_boolean = fhir_boolean_clone(self->deceased_boolean);
    }
    
    if (self->deceased_date_time) {
        clone->deceased_date_time = fhir_datetime_clone(self->deceased_date_time);
    }
    
    clone->address = fhir_array_clone((void**)self->address, self->address_count, 
                                     (FHIRCloneFunc)fhir_address_clone, &clone->address_count);
    
    clone->photo = fhir_array_clone((void**)self->photo, self->photo_count, 
                                   (FHIRCloneFunc)fhir_attachment_clone, &clone->photo_count);
    
    return clone;
}

/* ========================================================================== */
/* Practitioner Serialization Methods                                        */
/* ========================================================================== */

cJSON* fhir_practitioner_to_json(const FHIRPractitioner* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Practitioner is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "Practitioner") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add Practitioner-specific fields
    if (self->identifier && self->identifier_count > 0) {
        fhir_json_add_identifier_array(json, "identifier", self->identifier, self->identifier_count);
    }
    
    if (self->active) {
        fhir_json_add_boolean(json, "active", self->active);
    }
    
    if (self->name && self->name_count > 0) {
        fhir_json_add_humanname_array(json, "name", self->name, self->name_count);
    }
    
    if (self->telecom && self->telecom_count > 0) {
        fhir_json_add_contactpoint_array(json, "telecom", self->telecom, self->telecom_count);
    }
    
    // Add gender
    const char* gender_str = (self->gender == FHIR_PRACTITIONER_GENDER_MALE) ? "male" :
                            (self->gender == FHIR_PRACTITIONER_GENDER_FEMALE) ? "female" :
                            (self->gender == FHIR_PRACTITIONER_GENDER_OTHER) ? "other" : "unknown";
    fhir_json_add_string(json, "gender", gender_str);
    
    if (self->birth_date) {
        fhir_json_add_date(json, "birthDate", self->birth_date);
    }
    
    // Add deceased (choice type)
    if (self->deceased_boolean) {
        fhir_json_add_boolean(json, "deceasedBoolean", self->deceased_boolean);
    } else if (self->deceased_date_time) {
        fhir_json_add_datetime(json, "deceasedDateTime", self->deceased_date_time);
    }
    
    if (self->address && self->address_count > 0) {
        fhir_json_add_address_array(json, "address", self->address, self->address_count);
    }
    
    if (self->photo && self->photo_count > 0) {
        fhir_json_add_attachment_array(json, "photo", self->photo, self->photo_count);
    }
    
    return json;
}

bool fhir_practitioner_from_json(FHIRPractitioner* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "Practitioner") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse Practitioner-specific fields
    const cJSON* identifier_json = cJSON_GetObjectItem(json, "identifier");
    if (identifier_json && cJSON_IsArray(identifier_json)) {
        self->identifier = fhir_json_parse_identifier_array(identifier_json, &self->identifier_count);
    }
    
    const cJSON* active_json = cJSON_GetObjectItem(json, "active");
    if (active_json) {
        self->active = fhir_json_parse_boolean(active_json);
    }
    
    const cJSON* name_json = cJSON_GetObjectItem(json, "name");
    if (name_json && cJSON_IsArray(name_json)) {
        self->name = fhir_json_parse_humanname_array(name_json, &self->name_count);
    }
    
    const cJSON* telecom_json = cJSON_GetObjectItem(json, "telecom");
    if (telecom_json && cJSON_IsArray(telecom_json)) {
        self->telecom = fhir_json_parse_contactpoint_array(telecom_json, &self->telecom_count);
    }
    
    // Parse gender
    const char* gender_str = fhir_json_get_string(json, "gender");
    if (gender_str) {
        if (strcmp(gender_str, "male") == 0) {
            self->gender = FHIR_PRACTITIONER_GENDER_MALE;
        } else if (strcmp(gender_str, "female") == 0) {
            self->gender = FHIR_PRACTITIONER_GENDER_FEMALE;
        } else if (strcmp(gender_str, "other") == 0) {
            self->gender = FHIR_PRACTITIONER_GENDER_OTHER;
        } else {
            self->gender = FHIR_PRACTITIONER_GENDER_UNKNOWN;
        }
    }
    
    const cJSON* birth_date_json = cJSON_GetObjectItem(json, "birthDate");
    if (birth_date_json) {
        self->birth_date = fhir_json_parse_date(birth_date_json);
    }
    
    // Parse deceased (choice type)
    const cJSON* deceased_boolean_json = cJSON_GetObjectItem(json, "deceasedBoolean");
    if (deceased_boolean_json) {
        self->deceased_boolean = fhir_json_parse_boolean(deceased_boolean_json);
    }
    
    const cJSON* deceased_datetime_json = cJSON_GetObjectItem(json, "deceasedDateTime");
    if (deceased_datetime_json) {
        self->deceased_date_time = fhir_json_parse_datetime(deceased_datetime_json);
    }
    
    const cJSON* address_json = cJSON_GetObjectItem(json, "address");
    if (address_json && cJSON_IsArray(address_json)) {
        self->address = fhir_json_parse_address_array(address_json, &self->address_count);
    }
    
    return true;
}

FHIRPractitioner* fhir_practitioner_parse(const char* json_string) {
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
    
    FHIRPractitioner* practitioner = fhir_practitioner_create(id);
    if (!practitioner) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_practitioner_from_json(practitioner, json)) {
        fhir_practitioner_destroy(practitioner);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return practitioner;
}

/* ========================================================================== */
/* Practitioner Validation Methods                                           */
/* ========================================================================== */

bool fhir_practitioner_validate(const FHIRPractitioner* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("Practitioner", self->base.id)) {
        return false;
    }
    
    // Practitioner has no required fields beyond base resource
    return true;
}

/* ========================================================================== */
/* Practitioner-Specific Methods                                             */
/* ========================================================================== */

bool fhir_practitioner_is_active(const FHIRPractitioner* self) {
    if (!self || !self->active) return false;
    return self->active->value;
}

const char* fhir_practitioner_get_display_name(const FHIRPractitioner* self) {
    if (!self) return NULL;
    
    // Return first name if available
    if (self->name && self->name_count > 0 && self->name[0]) {
        FHIRHumanName* name = self->name[0];
        if (name->text && name->text->value) {
            return name->text->value;
        }
        // Construct name from parts if text not available
        // This would need more complex logic in a real implementation
    }
    
    return "Practitioner";
}

bool fhir_practitioner_is_deceased(const FHIRPractitioner* self) {
    if (!self) return false;
    
    if (self->deceased_boolean) {
        return self->deceased_boolean->value;
    }
    
    if (self->deceased_date_time) {
        return true; // If there's a death date, they're deceased
    }
    
    return false;
}

bool fhir_practitioner_add_qualification(FHIRPractitioner* self, 
                                        const FHIRPractitionerQualification* qualification) {
    if (!self || !qualification) return false;
    
    return fhir_array_add((void***)&self->qualification, &self->qualification_count,
                         (void*)qualification, sizeof(FHIRPractitionerQualification));
}

FHIRPractitionerQualification** fhir_practitioner_get_qualifications_by_code(
    const FHIRPractitioner* self, const char* code, size_t* count) {
    
    if (!self || !code || !count) {
        if (count) *count = 0;
        return NULL;
    }
    
    // This would need a more sophisticated implementation
    // For now, return all qualifications
    *count = self->qualification_count;
    return self->qualification;
}

bool fhir_practitioner_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_PRACTITIONER,
        .name = "Practitioner",
        .vtable = &Practitioner_vtable,
        .factory = (FHIRResourceFactory)fhir_practitioner_create
    };
    
    return fhir_resource_register_type(&registration);
}