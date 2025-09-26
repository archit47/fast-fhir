/**
 * @file fhir_patient.c
 * @brief FHIR R5 Patient resource C implementation with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "fhir_patient.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

/* ========================================================================== */
/* Static Data                                                               */
/* ========================================================================== */

static const char* g_gender_strings[] = {
    [FHIR_PATIENT_GENDER_UNKNOWN] = "unknown",
    [FHIR_PATIENT_GENDER_MALE] = "male",
    [FHIR_PATIENT_GENDER_FEMALE] = "female",
    [FHIR_PATIENT_GENDER_OTHER] = "other"
};

/* ========================================================================== */
/* Forward Declarations                                                       */
/* ========================================================================== */

static void fhir_patient_free_arrays(FHIRPatient* self);
static bool fhir_patient_validate_internal(const FHIRPatient* self, char*** errors, size_t* error_count);

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Patient, patient)

/* ========================================================================== */
/* Patient Factory and Lifecycle Methods                                     */
/* ========================================================================== */

FHIRPatient* fhir_patient_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_calloc(1, sizeof(FHIRPatient));
    if (!patient) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&patient->base, &Patient_vtable, FHIR_RESOURCE_TYPE_PATIENT, id)) {
        fhir_free(patient);
        return NULL;
    }
    
    // Initialize Patient-specific defaults
    patient->gender = FHIR_PATIENT_GENDER_UNKNOWN;
    
    return patient;
}

void fhir_patient_destroy(FHIRPatient* self) {
    if (!self) return;
    
    // Free Patient-specific fields
    fhir_patient_free_arrays(self);
    
    // Free choice type fields
    fhir_free(self->deceased_boolean);
    fhir_free(self->deceased_date_time);
    fhir_free(self->multiple_birth_boolean);
    fhir_free(self->multiple_birth_integer);
    
    // Free single fields
    fhir_free(self->active);
    fhir_free(self->birth_date);
    fhir_free(self->marital_status);
    fhir_free(self->managing_organization);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRPatient* fhir_patient_clone(const FHIRPatient* self) {
    if (!self) return NULL;
    
    FHIRPatient* clone = fhir_patient_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone Patient-specific fields
    if (self->active) {
        clone->active = fhir_malloc(sizeof(FHIRBoolean));
        if (clone->active) {
            clone->active->value = self->active->value;
        }
    }
    
    clone->gender = self->gender;
    
    if (self->birth_date) {
        clone->birth_date = fhir_malloc(sizeof(FHIRDate));
        if (clone->birth_date && self->birth_date->value) {
            clone->birth_date->value = fhir_strdup(self->birth_date->value);
        }
    }
    
    // Clone arrays (simplified - full implementation would deep copy all arrays)
    // For brevity, showing pattern for identifiers only
    if (self->identifier && self->identifier_count > 0) {
        clone->identifier = fhir_calloc(self->identifier_count, sizeof(FHIRIdentifier*));
        if (clone->identifier) {
            clone->identifier_count = self->identifier_count;
            for (size_t i = 0; i < self->identifier_count; i++) {
                if (self->identifier[i]) {
                    clone->identifier[i] = fhir_malloc(sizeof(FHIRIdentifier));
                    if (clone->identifier[i]) {
                        // Deep copy identifier (simplified)
                        memcpy(clone->identifier[i], self->identifier[i], sizeof(FHIRIdentifier));
                    }
                }
            }
        }
    }
    
    return clone;
}

/* ========================================================================== */
/* Private Helper Functions                                                   */
/* ========================================================================== */

static void fhir_patient_free_arrays(FHIRPatient* self) {
    if (!self) return;
    
    // Free identifier array
    if (self->identifier) {
        for (size_t i = 0; i < self->identifier_count; i++) {
            fhir_free(self->identifier[i]);
        }
        fhir_free(self->identifier);
    }
    
    // Free name array
    if (self->name) {
        for (size_t i = 0; i < self->name_count; i++) {
            fhir_free(self->name[i]);
        }
        fhir_free(self->name);
    }
    
    // Free telecom array
    if (self->telecom) {
        for (size_t i = 0; i < self->telecom_count; i++) {
            fhir_free(self->telecom[i]);
        }
        fhir_free(self->telecom);
    }
    
    // Free address array
    if (self->address) {
        for (size_t i = 0; i < self->address_count; i++) {
            fhir_free(self->address[i]);
        }
        fhir_free(self->address);
    }
    
    // Free photo array
    if (self->photo) {
        for (size_t i = 0; i < self->photo_count; i++) {
            fhir_free(self->photo[i]);
        }
        fhir_free(self->photo);
    }
    
    // Free contact array
    if (self->contact) {
        for (size_t i = 0; i < self->contact_count; i++) {
            fhir_free(self->contact[i]);
        }
        fhir_free(self->contact);
    }
    
    // Free communication array
    if (self->communication) {
        for (size_t i = 0; i < self->communication_count; i++) {
            fhir_free(self->communication[i]);
        }
        fhir_free(self->communication);
    }
    
    // Free general practitioner array
    if (self->general_practitioner) {
        for (size_t i = 0; i < self->general_practitioner_count; i++) {
            fhir_free(self->general_practitioner[i]);
        }
        fhir_free(self->general_practitioner);
    }
    
    // Free link array
    if (self->link) {
        for (size_t i = 0; i < self->link_count; i++) {
            fhir_free(self->link[i]);
        }
        fhir_free(self->link);
    }
}/* =====
===================================================================== */
/* Patient Serialization Methods                                             */
/* ========================================================================== */

cJSON* fhir_patient_to_json(const FHIRPatient* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Patient is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "Patient") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add active field
    if (self->active) {
        fhir_json_add_bool(json, "active", self->active->value);
    }
    
    // Add gender
    if (self->gender != FHIR_PATIENT_GENDER_UNKNOWN) {
        const char* gender_str = fhir_patient_gender_to_string(self->gender);
        if (gender_str) {
            fhir_json_add_string(json, "gender", gender_str);
        }
    }
    
    // Add birth date
    if (self->birth_date && self->birth_date->value) {
        fhir_json_add_string(json, "birthDate", self->birth_date->value);
    }
    
    // Add deceased information (choice type)
    if (self->deceased_boolean) {
        fhir_json_add_bool(json, "deceasedBoolean", self->deceased_boolean->value);
    } else if (self->deceased_date_time && self->deceased_date_time->value) {
        fhir_json_add_string(json, "deceasedDateTime", self->deceased_date_time->value);
    }
    
    // Add identifier array
    if (self->identifier && self->identifier_count > 0) {
        cJSON* identifier_array = cJSON_CreateArray();
        if (identifier_array) {
            for (size_t i = 0; i < self->identifier_count; i++) {
                if (self->identifier[i]) {
                    cJSON* identifier_json = cJSON_CreateObject();
                    if (identifier_json) {
                        // Serialize identifier (simplified)
                        cJSON_AddItemToArray(identifier_array, identifier_json);
                    }
                }
            }
            cJSON_AddItemToObject(json, "identifier", identifier_array);
        }
    }
    
    // Add name array
    if (self->name && self->name_count > 0) {
        cJSON* name_array = cJSON_CreateArray();
        if (name_array) {
            for (size_t i = 0; i < self->name_count; i++) {
                if (self->name[i]) {
                    cJSON* name_json = cJSON_CreateObject();
                    if (name_json) {
                        // Serialize name (simplified)
                        cJSON_AddItemToArray(name_array, name_json);
                    }
                }
            }
            cJSON_AddItemToObject(json, "name", name_array);
        }
    }
    
    return json;
}

bool fhir_patient_from_json(FHIRPatient* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "Patient") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse active field
    cJSON* active_json = cJSON_GetObjectItem(json, "active");
    if (active_json && cJSON_IsBool(active_json)) {
        self->active = fhir_malloc(sizeof(FHIRBoolean));
        if (self->active) {
            self->active->value = cJSON_IsTrue(active_json);
        }
    }
    
    // Parse gender
    const char* gender_str = fhir_json_get_string(json, "gender");
    if (gender_str) {
        self->gender = fhir_patient_gender_from_string(gender_str);
    }
    
    // Parse birth date
    const char* birth_date_str = fhir_json_get_string(json, "birthDate");
    if (birth_date_str) {
        if (fhir_validate_date(birth_date_str)) {
            self->birth_date = fhir_malloc(sizeof(FHIRDate));
            if (self->birth_date) {
                self->birth_date->value = fhir_strdup(birth_date_str);
            }
        }
    }
    
    // Parse deceased information (choice type)
    cJSON* deceased_bool_json = cJSON_GetObjectItem(json, "deceasedBoolean");
    if (deceased_bool_json && cJSON_IsBool(deceased_bool_json)) {
        self->deceased_boolean = fhir_malloc(sizeof(FHIRBoolean));
        if (self->deceased_boolean) {
            self->deceased_boolean->value = cJSON_IsTrue(deceased_bool_json);
        }
    } else {
        const char* deceased_datetime_str = fhir_json_get_string(json, "deceasedDateTime");
        if (deceased_datetime_str && fhir_validate_datetime(deceased_datetime_str)) {
            self->deceased_date_time = fhir_malloc(sizeof(FHIRDateTime));
            if (self->deceased_date_time) {
                self->deceased_date_time->value = fhir_strdup(deceased_datetime_str);
            }
        }
    }
    
    // Parse arrays (simplified implementation)
    cJSON* identifier_array = cJSON_GetObjectItem(json, "identifier");
    if (identifier_array && cJSON_IsArray(identifier_array)) {
        int array_size = cJSON_GetArraySize(identifier_array);
        if (array_size > 0) {
            self->identifier = fhir_calloc(array_size, sizeof(FHIRIdentifier*));
            if (self->identifier) {
                self->identifier_count = array_size;
                for (int i = 0; i < array_size; i++) {
                    cJSON* identifier_json = cJSON_GetArrayItem(identifier_array, i);
                    if (identifier_json && cJSON_IsObject(identifier_json)) {
                        self->identifier[i] = fhir_malloc(sizeof(FHIRIdentifier));
                        if (self->identifier[i]) {
                            // Parse identifier fields (simplified)
                        }
                    }
                }
            }
        }
    }
    
    return true;
}

FHIRPatient* fhir_patient_parse(const char* json_string) {
    if (!json_string) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "JSON string is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_JSON, "Failed to parse JSON");
        return NULL;
    }
    
    // Get ID from JSON
    const char* id = fhir_json_get_string(json, "id");
    if (!id) {
        cJSON_Delete(json);
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "id");
        return NULL;
    }
    
    FHIRPatient* patient = fhir_patient_create(id);
    if (!patient) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_patient_from_json(patient, json)) {
        fhir_patient_destroy(patient);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return patient;
}/* =========
================================================================= */
/* Patient Validation Methods                                                */
/* ========================================================================== */

bool fhir_patient_validate(const FHIRPatient* self) {
    if (!self) return false;
    
    // Use cached validation if available
    if (self->base.validation_cached) {
        return self->base.validation_result;
    }
    
    char** errors = NULL;
    size_t error_count = 0;
    bool is_valid = fhir_patient_validate_internal(self, &errors, &error_count);
    
    // Cache validation result
    FHIRPatient* mutable_self = (FHIRPatient*)self; // Cast away const for caching
    mutable_self->base.validation_cached = true;
    mutable_self->base.validation_result = is_valid;
    mutable_self->base.validation_errors = errors;
    mutable_self->base.validation_error_count = error_count;
    
    return is_valid;
}

static bool fhir_patient_validate_internal(const FHIRPatient* self, char*** errors, size_t* error_count) {
    if (!self || !errors || !error_count) return false;
    
    *errors = NULL;
    *error_count = 0;
    bool is_valid = true;
    
    // Validate base resource
    if (!fhir_validate_base_resource("Patient", self->base.id)) {
        is_valid = false;
        // Add base validation errors
    }
    
    // Validate birth date format if present
    if (self->birth_date && self->birth_date->value) {
        if (!fhir_validate_date(self->birth_date->value)) {
            is_valid = false;
            // Add error to list
        }
    }
    
    // Validate that deceased choice type has only one value
    if (self->deceased_boolean && self->deceased_date_time) {
        is_valid = false;
        // Add error: "Patient can have either deceasedBoolean or deceasedDateTime, not both"
    }
    
    // Validate that multiple birth choice type has only one value
    if (self->multiple_birth_boolean && self->multiple_birth_integer) {
        is_valid = false;
        // Add error: "Patient can have either multipleBirthBoolean or multipleBirthInteger, not both"
    }
    
    // Additional FHIR-specific validations would go here
    
    return is_valid;
}

char** fhir_patient_get_validation_errors(const FHIRPatient* self, size_t* count) {
    if (!self || !count) {
        if (count) *count = 0;
        return NULL;
    }
    
    // Ensure validation has been run
    fhir_patient_validate(self);
    
    *count = self->base.validation_error_count;
    return self->base.validation_errors;
}

/* ========================================================================== */
/* Patient Comparison Methods                                                */
/* ========================================================================== */

bool fhir_patient_equals(const FHIRPatient* self, const FHIRPatient* other) {
    if (self == other) return true;
    if (!self || !other) return false;
    
    // Compare IDs
    if (fhir_strcmp(self->base.id, other->base.id) != 0) return false;
    
    // Compare active status
    if ((self->active == NULL) != (other->active == NULL)) return false;
    if (self->active && other->active && self->active->value != other->active->value) return false;
    
    // Compare gender
    if (self->gender != other->gender) return false;
    
    // Compare birth date
    if ((self->birth_date == NULL) != (other->birth_date == NULL)) return false;
    if (self->birth_date && other->birth_date) {
        if (fhir_strcmp(self->birth_date->value, other->birth_date->value) != 0) return false;
    }
    
    // Additional field comparisons would go here
    
    return true;
}

int fhir_patient_compare(const FHIRPatient* self, const FHIRPatient* other) {
    if (self == other) return 0;
    if (!self) return -1;
    if (!other) return 1;
    
    // Compare by ID first
    int id_cmp = fhir_strcmp(self->base.id, other->base.id);
    if (id_cmp != 0) return id_cmp;
    
    // Compare by birth date if available
    if (self->birth_date && other->birth_date) {
        return fhir_strcmp(self->birth_date->value, other->birth_date->value);
    }
    
    if (self->birth_date && !other->birth_date) return 1;
    if (!self->birth_date && other->birth_date) return -1;
    
    return 0;
}

/* ========================================================================== */
/* Patient String Representation                                             */
/* ========================================================================== */

char* fhir_patient_to_string(const FHIRPatient* self) {
    if (!self) return NULL;
    
    const char* display_name = fhir_patient_get_display_name(self);
    const char* gender_str = fhir_patient_gender_to_string(self->gender);
    
    char* result = fhir_malloc(256);
    if (!result) return NULL;
    
    snprintf(result, 256, "Patient(id=%s, name=%s, gender=%s, active=%s)",
             self->base.id ? self->base.id : "unknown",
             display_name ? display_name : "unknown",
             gender_str ? gender_str : "unknown",
             (self->active && self->active->value) ? "true" : "false");
    
    return result;
}

/* ========================================================================== */
/* Patient-Specific Methods                                                  */
/* ========================================================================== */

bool fhir_patient_is_active(const FHIRPatient* self) {
    if (!self || !self->active) return false;
    return self->active->value;
}

const char* fhir_patient_get_display_name(const FHIRPatient* self) {
    if (!self || !self->name || self->name_count == 0) return NULL;
    
    // Find the first official or usual name
    for (size_t i = 0; i < self->name_count; i++) {
        if (self->name[i]) {
            // Return first available name (simplified)
            // In full implementation, would check name use and return formatted name
            return "Patient Name"; // Placeholder
        }
    }
    
    return NULL;
}

bool fhir_patient_is_deceased(const FHIRPatient* self) {
    if (!self) return false;
    
    if (self->deceased_boolean) {
        return self->deceased_boolean->value;
    }
    
    if (self->deceased_date_time && self->deceased_date_time->value) {
        return true; // If there's a death date, patient is deceased
    }
    
    return false;
}

int fhir_patient_get_age(const FHIRPatient* self) {
    if (!self || !self->birth_date || !self->birth_date->value) return -1;
    
    // Parse birth date and calculate age (simplified implementation)
    // In full implementation, would properly parse date and calculate age
    return -1; // Placeholder
}

const FHIRHumanName* fhir_patient_get_primary_name(const FHIRPatient* self) {
    if (!self || !self->name || self->name_count == 0) return NULL;
    
    // Return first name (simplified)
    return self->name[0];
}

const FHIRAddress* fhir_patient_get_primary_address(const FHIRPatient* self) {
    if (!self || !self->address || self->address_count == 0) return NULL;
    
    // Return first address (simplified)
    return self->address[0];
}/* =
========================================================================= */
/* Patient Modification Methods                                              */
/* ========================================================================== */

bool fhir_patient_set_active(FHIRPatient* self, bool active) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Patient is NULL");
        return false;
    }
    
    if (!self->active) {
        self->active = fhir_malloc(sizeof(FHIRBoolean));
        if (!self->active) return false;
    }
    
    self->active->value = active;
    
    // Clear validation cache
    self->base.validation_cached = false;
    
    return true;
}

bool fhir_patient_set_gender(FHIRPatient* self, FHIRPatientGender gender) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Patient is NULL");
        return false;
    }
    
    if (gender < FHIR_PATIENT_GENDER_UNKNOWN || gender > FHIR_PATIENT_GENDER_OTHER) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid gender value");
        return false;
    }
    
    self->gender = gender;
    
    // Clear validation cache
    self->base.validation_cached = false;
    
    return true;
}

bool fhir_patient_set_birth_date(FHIRPatient* self, const char* birth_date) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Patient is NULL");
        return false;
    }
    
    if (!birth_date) {
        // Clear birth date
        fhir_free(self->birth_date);
        self->birth_date = NULL;
        return true;
    }
    
    if (!fhir_validate_date(birth_date)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid date format", "birthDate");
        return false;
    }
    
    if (!self->birth_date) {
        self->birth_date = fhir_malloc(sizeof(FHIRDate));
        if (!self->birth_date) return false;
    } else {
        fhir_free(self->birth_date->value);
    }
    
    self->birth_date->value = fhir_strdup(birth_date);
    if (!self->birth_date->value) {
        fhir_free(self->birth_date);
        self->birth_date = NULL;
        return false;
    }
    
    // Clear validation cache
    self->base.validation_cached = false;
    
    return true;
}

bool fhir_patient_add_identifier(FHIRPatient* self, const FHIRIdentifier* identifier) {
    if (!self || !identifier) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return fhir_array_add((void**)&self->identifier, &self->identifier_count, 
                         identifier, sizeof(FHIRIdentifier*));
}

bool fhir_patient_add_name(FHIRPatient* self, const FHIRHumanName* name) {
    if (!self || !name) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return fhir_array_add((void**)&self->name, &self->name_count, 
                         name, sizeof(FHIRHumanName*));
}

bool fhir_patient_add_address(FHIRPatient* self, const FHIRAddress* address) {
    if (!self || !address) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return fhir_array_add((void**)&self->address, &self->address_count, 
                         address, sizeof(FHIRAddress*));
}

bool fhir_patient_add_telecom(FHIRPatient* self, const FHIRContactPoint* telecom) {
    if (!self || !telecom) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    return fhir_array_add((void**)&self->telecom, &self->telecom_count, 
                         telecom, sizeof(FHIRContactPoint*));
}

/* ========================================================================== */
/* Patient Utility Functions                                                 */
/* ========================================================================== */

const char* fhir_patient_gender_to_string(FHIRPatientGender gender) {
    if (gender >= 0 && gender < (sizeof(g_gender_strings) / sizeof(g_gender_strings[0]))) {
        return g_gender_strings[gender];
    }
    return NULL;
}

FHIRPatientGender fhir_patient_gender_from_string(const char* gender_str) {
    if (!gender_str) return FHIR_PATIENT_GENDER_UNKNOWN;
    
    for (int i = 0; i < (sizeof(g_gender_strings) / sizeof(g_gender_strings[0])); i++) {
        if (g_gender_strings[i] && strcmp(gender_str, g_gender_strings[i]) == 0) {
            return (FHIRPatientGender)i;
        }
    }
    
    return FHIR_PATIENT_GENDER_UNKNOWN;
}

bool fhir_patient_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_PATIENT,
        .name = "Patient",
        .vtable = &Patient_vtable,
        .factory = (FHIRResourceFactory)fhir_patient_create
    };
    
    return fhir_resource_register_type(&registration);
}