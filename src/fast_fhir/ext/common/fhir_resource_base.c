/**
 * @file fhir_resource_base.c
 * @brief Base resource system implementation with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "fhir_resource_base.h"
#include "fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Global Resource Registry                                                   */
/* ========================================================================== */

static FHIRResourceRegistration g_resource_registry[FHIR_RESOURCE_TYPE_COUNT];
static bool g_registry_initialized = false;

/* Resource type name mapping */
static const char* g_resource_type_names[FHIR_RESOURCE_TYPE_COUNT] = {
    [FHIR_RESOURCE_TYPE_UNKNOWN] = "Unknown",
    [FHIR_RESOURCE_TYPE_PATIENT] = "Patient",
    [FHIR_RESOURCE_TYPE_PRACTITIONER] = "Practitioner",
    [FHIR_RESOURCE_TYPE_PRACTITIONER_ROLE] = "PractitionerRole",
    [FHIR_RESOURCE_TYPE_ORGANIZATION] = "Organization",
    [FHIR_RESOURCE_TYPE_ORGANIZATION_AFFILIATION] = "OrganizationAffiliation",
    [FHIR_RESOURCE_TYPE_LOCATION] = "Location",
    [FHIR_RESOURCE_TYPE_HEALTHCARE_SERVICE] = "HealthcareService",
    [FHIR_RESOURCE_TYPE_ENDPOINT] = "Endpoint",
    [FHIR_RESOURCE_TYPE_RELATED_PERSON] = "RelatedPerson",
    [FHIR_RESOURCE_TYPE_PERSON] = "Person",
    [FHIR_RESOURCE_TYPE_GROUP] = "Group",
    [FHIR_RESOURCE_TYPE_ENCOUNTER] = "Encounter",
    [FHIR_RESOURCE_TYPE_ENCOUNTER_HISTORY] = "EncounterHistory",
    [FHIR_RESOURCE_TYPE_EPISODE_OF_CARE] = "EpisodeOfCare",
    [FHIR_RESOURCE_TYPE_OBSERVATION] = "Observation",
    [FHIR_RESOURCE_TYPE_CONDITION] = "Condition",
    [FHIR_RESOURCE_TYPE_PROCEDURE] = "Procedure",
    [FHIR_RESOURCE_TYPE_DIAGNOSTIC_REPORT] = "DiagnosticReport",
    [FHIR_RESOURCE_TYPE_APPOINTMENT] = "Appointment",
    [FHIR_RESOURCE_TYPE_APPOINTMENT_RESPONSE] = "AppointmentResponse",
    [FHIR_RESOURCE_TYPE_SCHEDULE] = "Schedule",
    [FHIR_RESOURCE_TYPE_SLOT] = "Slot",
    [FHIR_RESOURCE_TYPE_TASK] = "Task",
    [FHIR_RESOURCE_TYPE_TRANSPORT] = "Transport",
    [FHIR_RESOURCE_TYPE_DEVICE] = "Device",
    [FHIR_RESOURCE_TYPE_DEVICE_METRIC] = "DeviceMetric",
    [FHIR_RESOURCE_TYPE_BIOLOGICALLY_DERIVED_PRODUCT] = "BiologicallyDerivedProduct",
    [FHIR_RESOURCE_TYPE_NUTRITION_PRODUCT] = "NutritionProduct",
    [FHIR_RESOURCE_TYPE_VERIFICATION_RESULT] = "VerificationResult"
};

/* ========================================================================== */
/* Private Helper Functions                                                   */
/* ========================================================================== */

static void init_registry_if_needed(void) {
    if (!g_registry_initialized) {
        memset(g_resource_registry, 0, sizeof(g_resource_registry));
        g_registry_initialized = true;
    }
}

static void free_validation_errors(FHIRResourceBase* self) {
    if (self->validation_errors) {
        for (size_t i = 0; i < self->validation_error_count; i++) {
            fhir_free(self->validation_errors[i]);
        }
        fhir_free(self->validation_errors);
        self->validation_errors = NULL;
        self->validation_error_count = 0;
    }
}

/* ========================================================================== */
/* Resource Registry Implementation                                           */
/* ========================================================================== */

bool fhir_resource_register_type(const FHIRResourceRegistration* registration) {
    if (!registration || registration->type <= FHIR_RESOURCE_TYPE_UNKNOWN || 
        registration->type >= FHIR_RESOURCE_TYPE_COUNT) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid registration");
        return false;
    }
    
    init_registry_if_needed();
    
    if (g_resource_registry[registration->type].type != FHIR_RESOURCE_TYPE_UNKNOWN) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Resource type already registered");
        return false;
    }
    
    g_resource_registry[registration->type] = *registration;
    return true;
}

FHIRResourceBase* fhir_resource_create_by_name(const char* type_name, const char* id) {
    if (!type_name) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Type name is NULL");
        return NULL;
    }
    
    FHIRResourceType type = fhir_resource_type_from_string(type_name);
    return fhir_resource_create_by_type(type, id);
}

FHIRResourceBase* fhir_resource_create_by_type(FHIRResourceType type, const char* id) {
    if (type <= FHIR_RESOURCE_TYPE_UNKNOWN || type >= FHIR_RESOURCE_TYPE_COUNT) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid resource type");
        return NULL;
    }
    
    init_registry_if_needed();
    
    const FHIRResourceRegistration* reg = &g_resource_registry[type];
    if (reg->type == FHIR_RESOURCE_TYPE_UNKNOWN || !reg->factory) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Resource type not registered");
        return NULL;
    }
    
    return reg->factory(id);
}/* ====
====================================================================== */
/* Base Resource Implementation                                               */
/* ========================================================================== */

bool fhir_resource_base_init(FHIRResourceBase* self, const FHIRResourceVTable* vtable,
                            FHIRResourceType type, const char* id) {
    if (!self || !vtable || !id) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return false;
    }
    
    // Initialize base fields
    memset(self, 0, sizeof(FHIRResourceBase));
    self->vtable = vtable;
    self->ref_count = 1;
    self->resource_type = type;
    self->is_domain_resource = true; // Most FHIR resources are DomainResources
    
    // Set ID
    self->id = fhir_strdup(id);
    if (!self->id) {
        return false;
    }
    
    return true;
}

void fhir_resource_base_cleanup(FHIRResourceBase* self) {
    if (!self) return;
    
    // Free base resource fields
    fhir_free(self->id);
    fhir_free(self->meta);
    fhir_free(self->implicit_rules);
    fhir_free(self->language);
    fhir_free(self->text);
    
    // Free contained resources
    if (self->contained) {
        for (size_t i = 0; i < self->contained_count; i++) {
            if (self->contained[i]) {
                fhir_resource_release((FHIRResourceBase*)self->contained[i]);
            }
        }
        fhir_free(self->contained);
    }
    
    // Free extensions
    if (self->extension) {
        for (size_t i = 0; i < self->extension_count; i++) {
            fhir_free(self->extension[i]);
        }
        fhir_free(self->extension);
    }
    
    if (self->modifier_extension) {
        for (size_t i = 0; i < self->modifier_extension_count; i++) {
            fhir_free(self->modifier_extension[i]);
        }
        fhir_free(self->modifier_extension);
    }
    
    // Free validation errors
    free_validation_errors(self);
}

FHIRResourceBase* fhir_resource_retain(FHIRResourceBase* self) {
    if (self) {
        self->ref_count++;
    }
    return self;
}

void fhir_resource_release(FHIRResourceBase* self) {
    if (!self) return;
    
    self->ref_count--;
    if (self->ref_count <= 0) {
        // Call virtual destructor
        if (self->vtable && self->vtable->destroy) {
            self->vtable->destroy(self);
        } else {
            // Fallback cleanup
            fhir_resource_base_cleanup(self);
            fhir_free(self);
        }
    }
}

int fhir_resource_get_ref_count(const FHIRResourceBase* self) {
    return self ? self->ref_count : 0;
}

/* ========================================================================== */
/* Utility Functions Implementation                                          */
/* ========================================================================== */

const char* fhir_resource_type_to_string(FHIRResourceType type) {
    if (type >= 0 && type < FHIR_RESOURCE_TYPE_COUNT) {
        return g_resource_type_names[type];
    }
    return NULL;
}

FHIRResourceType fhir_resource_type_from_string(const char* name) {
    if (!name) return FHIR_RESOURCE_TYPE_UNKNOWN;
    
    for (int i = 1; i < FHIR_RESOURCE_TYPE_COUNT; i++) {
        if (g_resource_type_names[i] && strcmp(name, g_resource_type_names[i]) == 0) {
            return (FHIRResourceType)i;
        }
    }
    
    return FHIR_RESOURCE_TYPE_UNKNOWN;
}

bool fhir_resource_type_is_valid(FHIRResourceType type) {
    return type > FHIR_RESOURCE_TYPE_UNKNOWN && type < FHIR_RESOURCE_TYPE_COUNT;
}

size_t fhir_resource_get_instance_size(FHIRResourceType type) {
    if (type <= FHIR_RESOURCE_TYPE_UNKNOWN || type >= FHIR_RESOURCE_TYPE_COUNT) {
        return 0;
    }
    
    init_registry_if_needed();
    
    const FHIRResourceRegistration* reg = &g_resource_registry[type];
    if (reg->vtable) {
        return reg->vtable->instance_size;
    }
    
    return 0;
}