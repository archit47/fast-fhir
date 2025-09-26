/**
 * @file fhir_resource_base.h
 * @brief Base resource system with OOP principles for FHIR C extensions
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * This header defines the base resource system implementing Object-Oriented
 * Programming principles in C for FHIR resources.
 */

#ifndef FHIR_RESOURCE_BASE_H
#define FHIR_RESOURCE_BASE_H

#include "fhir_common.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>
#include <cjson/cJSON.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/* Forward Declarations                                                       */
/* ========================================================================== */

typedef struct FHIRResourceVTable FHIRResourceVTable;
typedef struct FHIRResourceBase FHIRResourceBase;

/* ========================================================================== */
/* Resource Type Enumeration                                                 */
/* ========================================================================== */

typedef enum {
    FHIR_RESOURCE_TYPE_UNKNOWN = 0,
    
    // Foundation Resources
    FHIR_RESOURCE_TYPE_PATIENT,
    FHIR_RESOURCE_TYPE_PRACTITIONER,
    FHIR_RESOURCE_TYPE_PRACTITIONER_ROLE,
    FHIR_RESOURCE_TYPE_ORGANIZATION,
    FHIR_RESOURCE_TYPE_ORGANIZATION_AFFILIATION,
    FHIR_RESOURCE_TYPE_LOCATION,
    FHIR_RESOURCE_TYPE_HEALTHCARE_SERVICE,
    FHIR_RESOURCE_TYPE_ENDPOINT,
    FHIR_RESOURCE_TYPE_RELATED_PERSON,
    FHIR_RESOURCE_TYPE_PERSON,
    FHIR_RESOURCE_TYPE_GROUP,
    
    // Clinical Resources
    FHIR_RESOURCE_TYPE_ENCOUNTER,
    FHIR_RESOURCE_TYPE_ENCOUNTER_HISTORY,
    FHIR_RESOURCE_TYPE_EPISODE_OF_CARE,
    FHIR_RESOURCE_TYPE_OBSERVATION,
    FHIR_RESOURCE_TYPE_CONDITION,
    FHIR_RESOURCE_TYPE_PROCEDURE,
    FHIR_RESOURCE_TYPE_DIAGNOSTIC_REPORT,
    
    // Workflow Resources
    FHIR_RESOURCE_TYPE_APPOINTMENT,
    FHIR_RESOURCE_TYPE_APPOINTMENT_RESPONSE,
    FHIR_RESOURCE_TYPE_SCHEDULE,
    FHIR_RESOURCE_TYPE_SLOT,
    FHIR_RESOURCE_TYPE_TASK,
    FHIR_RESOURCE_TYPE_TRANSPORT,
    
    // Specialized Resources
    FHIR_RESOURCE_TYPE_DEVICE,
    FHIR_RESOURCE_TYPE_DEVICE_METRIC,
    FHIR_RESOURCE_TYPE_BIOLOGICALLY_DERIVED_PRODUCT,
    FHIR_RESOURCE_TYPE_NUTRITION_PRODUCT,
    FHIR_RESOURCE_TYPE_VERIFICATION_RESULT,
    
    FHIR_RESOURCE_TYPE_COUNT
} FHIRResourceType;

/* ========================================================================== */
/* Virtual Function Table (VTable) - OOP Method Dispatch                    */
/* ========================================================================== */

/**
 * @brief Virtual function table for FHIR resources
 * 
 * This structure implements polymorphism in C by providing function pointers
 * for virtual methods that can be overridden by derived resource types.
 */struct F
HIRResourceVTable {
    // Resource lifecycle methods
    void (*destroy)(FHIRResourceBase* self);
    FHIRResourceBase* (*clone)(const FHIRResourceBase* self);
    
    // Serialization methods
    cJSON* (*to_json)(const FHIRResourceBase* self);
    bool (*from_json)(FHIRResourceBase* self, const cJSON* json);
    
    // Validation methods
    bool (*validate)(const FHIRResourceBase* self);
    char** (*get_validation_errors)(const FHIRResourceBase* self, size_t* count);
    
    // Comparison methods
    bool (*equals)(const FHIRResourceBase* self, const FHIRResourceBase* other);
    int (*compare)(const FHIRResourceBase* self, const FHIRResourceBase* other);
    
    // String representation
    char* (*to_string)(const FHIRResourceBase* self);
    
    // Resource-specific methods (can be NULL if not applicable)
    bool (*is_active)(const FHIRResourceBase* self);
    const char* (*get_display_name)(const FHIRResourceBase* self);
    
    // Type information
    const char* resource_type_name;
    FHIRResourceType resource_type;
    size_t instance_size;
};

/* ========================================================================== */
/* Base Resource Structure                                                    */
/* ========================================================================== */

/**
 * @brief Base structure for all FHIR resources
 * 
 * This structure implements the base class for all FHIR resources,
 * providing common fields and virtual method dispatch.
 */
struct FHIRResourceBase {
    // Virtual function table (must be first for polymorphism)
    const FHIRResourceVTable* vtable;
    
    // Reference counting for memory management
    int ref_count;
    
    // Base FHIR Resource fields
    char* id;
    FHIRMeta* meta;
    FHIRUri* implicit_rules;
    FHIRCode* language;
    
    // DomainResource fields (most resources inherit from DomainResource)
    FHIRNarrative* text;
    FHIRResource** contained;
    size_t contained_count;
    FHIRExtension** extension;
    size_t extension_count;
    FHIRExtension** modifier_extension;
    size_t modifier_extension_count;
    
    // Internal fields
    bool is_domain_resource;
    FHIRResourceType resource_type;
    
    // Validation cache
    bool validation_cached;
    bool validation_result;
    char** validation_errors;
    size_t validation_error_count;
};

/* ========================================================================== */
/* Resource Factory and Registry                                             */
/* ========================================================================== */

/**
 * @brief Resource factory function type
 */
typedef FHIRResourceBase* (*FHIRResourceFactory)(const char* id);

/**
 * @brief Resource registration structure
 */
typedef struct {
    FHIRResourceType type;
    const char* name;
    const FHIRResourceVTable* vtable;
    FHIRResourceFactory factory;
} FHIRResourceRegistration;

/**
 * @brief Register a resource type
 * @param registration Resource registration information
 * @return true on success, false on failure
 */
bool fhir_resource_register_type(const FHIRResourceRegistration* registration);

/**
 * @brief Create resource by type name
 * @param type_name Resource type name
 * @param id Resource ID
 * @return New resource instance or NULL on failure
 */
FHIRResourceBase* fhir_resource_create_by_name(const char* type_name, const char* id);

/**
 * @brief Create resource by type enum
 * @param type Resource type
 * @param id Resource ID
 * @return New resource instance or NULL on failure
 */
FHIRResourceBase* fhir_resource_create_by_type(FHIRResourceType type, const char* id);/*
 ========================================================================== */
/* Base Resource Methods (OOP Interface)                                     */
/* ========================================================================== */

/**
 * @brief Initialize base resource
 * @param self Resource instance
 * @param vtable Virtual function table
 * @param type Resource type
 * @param id Resource ID
 * @return true on success, false on failure
 */
bool fhir_resource_base_init(FHIRResourceBase* self, const FHIRResourceVTable* vtable,
                            FHIRResourceType type, const char* id);

/**
 * @brief Cleanup base resource (called by derived destructors)
 * @param self Resource instance
 */
void fhir_resource_base_cleanup(FHIRResourceBase* self);

/**
 * @brief Add reference to resource (reference counting)
 * @param self Resource instance
 * @return Resource instance (for chaining)
 */
FHIRResourceBase* fhir_resource_retain(FHIRResourceBase* self);

/**
 * @brief Remove reference from resource (reference counting)
 * @param self Resource instance
 */
void fhir_resource_release(FHIRResourceBase* self);

/**
 * @brief Get reference count
 * @param self Resource instance
 * @return Reference count
 */
int fhir_resource_get_ref_count(const FHIRResourceBase* self);

/* ========================================================================== */
/* Polymorphic Method Calls (Virtual Method Dispatch)                       */
/* ========================================================================== */

/**
 * @brief Destroy resource (calls virtual destructor)
 * @param self Resource instance
 */
static inline void fhir_resource_destroy(FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->destroy) {
        self->vtable->destroy(self);
    }
}

/**
 * @brief Clone resource (calls virtual clone method)
 * @param self Resource instance
 * @return Cloned resource or NULL on failure
 */
static inline FHIRResourceBase* fhir_resource_clone(const FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->clone) {
        return self->vtable->clone(self);
    }
    return NULL;
}

/**
 * @brief Convert resource to JSON (calls virtual method)
 * @param self Resource instance
 * @return JSON object or NULL on failure
 */
static inline cJSON* fhir_resource_to_json(const FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->to_json) {
        return self->vtable->to_json(self);
    }
    return NULL;
}

/**
 * @brief Load resource from JSON (calls virtual method)
 * @param self Resource instance
 * @param json JSON object
 * @return true on success, false on failure
 */
static inline bool fhir_resource_from_json(FHIRResourceBase* self, const cJSON* json) {
    if (self && self->vtable && self->vtable->from_json) {
        return self->vtable->from_json(self, json);
    }
    return false;
}

/**
 * @brief Validate resource (calls virtual method)
 * @param self Resource instance
 * @return true if valid, false otherwise
 */
static inline bool fhir_resource_validate(const FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->validate) {
        return self->vtable->validate(self);
    }
    return false;
}/**
 * @b
rief Check if resource is active (calls virtual method)
 * @param self Resource instance
 * @return true if active, false otherwise
 */
static inline bool fhir_resource_is_active(const FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->is_active) {
        return self->vtable->is_active(self);
    }
    return false;
}

/**
 * @brief Get resource display name (calls virtual method)
 * @param self Resource instance
 * @return Display name or NULL
 */
static inline const char* fhir_resource_get_display_name(const FHIRResourceBase* self) {
    if (self && self->vtable && self->vtable->get_display_name) {
        return self->vtable->get_display_name(self);
    }
    return NULL;
}

/**
 * @brief Compare two resources (calls virtual method)
 * @param self First resource
 * @param other Second resource
 * @return true if equal, false otherwise
 */
static inline bool fhir_resource_equals(const FHIRResourceBase* self, const FHIRResourceBase* other) {
    if (self && other && self->vtable && self->vtable->equals) {
        return self->vtable->equals(self, other);
    }
    return self == other;
}

/* ========================================================================== */
/* Utility Functions                                                         */
/* ========================================================================== */

/**
 * @brief Get resource type name
 * @param type Resource type
 * @return Type name or NULL for unknown type
 */
const char* fhir_resource_type_to_string(FHIRResourceType type);

/**
 * @brief Get resource type from name
 * @param name Type name
 * @return Resource type or FHIR_RESOURCE_TYPE_UNKNOWN
 */
FHIRResourceType fhir_resource_type_from_string(const char* name);

/**
 * @brief Check if resource type is valid
 * @param type Resource type
 * @return true if valid, false otherwise
 */
bool fhir_resource_type_is_valid(FHIRResourceType type);

/**
 * @brief Get resource instance size
 * @param type Resource type
 * @return Instance size in bytes or 0 for unknown type
 */
size_t fhir_resource_get_instance_size(FHIRResourceType type);

/* ========================================================================== */
/* Macros for Resource Implementation                                        */
/* ========================================================================== */

/**
 * @brief Macro to define a resource structure with proper inheritance
 */
#define FHIR_RESOURCE_DEFINE(ResourceName) \
    typedef struct FHIR##ResourceName { \
        FHIRResourceBase base; \
        /* Resource-specific fields follow */ \
    } FHIR##ResourceName;

/**
 * @brief Macro to implement virtual method dispatch
 */
#define FHIR_RESOURCE_VTABLE_INIT(ResourceName, resource_type) \
    static const FHIRResourceVTable ResourceName##_vtable = { \
        .destroy = (void (*)(FHIRResourceBase*))fhir_##resource_type##_destroy, \
        .clone = (FHIRResourceBase* (*)(const FHIRResourceBase*))fhir_##resource_type##_clone, \
        .to_json = (cJSON* (*)(const FHIRResourceBase*))fhir_##resource_type##_to_json, \
        .from_json = (bool (*)(FHIRResourceBase*, const cJSON*))fhir_##resource_type##_from_json, \
        .validate = (bool (*)(const FHIRResourceBase*))fhir_##resource_type##_validate, \
        .equals = (bool (*)(const FHIRResourceBase*, const FHIRResourceBase*))fhir_##resource_type##_equals, \
        .to_string = (char* (*)(const FHIRResourceBase*))fhir_##resource_type##_to_string, \
        .is_active = (bool (*)(const FHIRResourceBase*))fhir_##resource_type##_is_active, \
        .get_display_name = (const char* (*)(const FHIRResourceBase*))fhir_##resource_type##_get_display_name, \
        .resource_type_name = #ResourceName, \
        .resource_type = FHIR_RESOURCE_TYPE_##ResourceName, \
        .instance_size = sizeof(FHIR##ResourceName) \
    };

#ifdef __cplusplus
}
#endif

#endif /* FHIR_RESOURCE_BASE_H */