/**
 * @file fhir_organization.c
 * @brief FHIR R5 Organization resource C implementation with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "fhir_organization.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Organization, organization)

/* ========================================================================== */
/* Organization Factory and Lifecycle Methods                             */
/* ========================================================================== */

FHIROrganization* fhir_organization_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIROrganization* organization = fhir_calloc(1, sizeof(FHIROrganization));
    if (!organization) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&organization->base, &Organization_vtable, 
                                FHIR_RESOURCE_TYPE_ORGANIZATION, id)) {
        fhir_free(organization);
        return NULL;
    }
    
    // Initialize Organization-specific defaults
    organization->active = fhir_boolean_create(true);
    
    return organization;
}

void fhir_organization_destroy(FHIROrganization* self) {
    if (!self) return;
    
    // Free Organization-specific fields
    if (self->active) fhir_boolean_destroy(self->active);
    if (self->name) fhir_string_destroy(self->name);
    if (self->description) fhir_markdown_destroy(self->description);
    if (self->part_of) fhir_reference_destroy(self->part_of);
    
    // Free arrays
    fhir_array_destroy((void**)self->type, self->type_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->alias, self->alias_count, (FHIRDestroyFunc)fhir_string_destroy);
    fhir_array_destroy((void**)self->contact, self->contact_count, (FHIRDestroyFunc)fhir_extendedcontactdetail_destroy);
    fhir_array_destroy((void**)self->endpoint, self->endpoint_count, (FHIRDestroyFunc)fhir_reference_destroy);
    fhir_array_destroy((void**)self->qualification, self->qualification_count, (FHIRDestroyFunc)fhir_organizationqualification_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIROrganization* fhir_organization_clone(const FHIROrganization* self) {
    if (!self) return NULL;
    
    FHIROrganization* clone = fhir_organization_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone Organization-specific fields
    if (self->active) {
        clone->active = fhir_boolean_clone(self->active);
    }
    if (self->name) {
        clone->name = fhir_string_clone(self->name);
    }
    if (self->description) {
        clone->description = fhir_markdown_clone(self->description);
    }
    if (self->part_of) {
        clone->part_of = fhir_reference_clone(self->part_of);
    }
    
    // Clone arrays
    clone->type = fhir_array_clone((void**)self->type, self->type_count, 
                                  (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->type_count);
    clone->alias = fhir_array_clone((void**)self->alias, self->alias_count, 
                                   (FHIRCloneFunc)fhir_string_clone, &clone->alias_count);
    clone->contact = fhir_array_clone((void**)self->contact, self->contact_count, 
                                     (FHIRCloneFunc)fhir_extendedcontactdetail_clone, &clone->contact_count);
    clone->endpoint = fhir_array_clone((void**)self->endpoint, self->endpoint_count, 
                                      (FHIRCloneFunc)fhir_reference_clone, &clone->endpoint_count);
    
    return clone;
}

/* ========================================================================== */
/* Organization Serialization Methods                                     */
/* ========================================================================== */

cJSON* fhir_organization_to_json(const FHIROrganization* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Organization is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "Organization") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add Organization-specific fields
    if (self->active) {
        fhir_json_add_boolean(json, "active", self->active);
    }
    if (self->name) {
        fhir_json_add_string_value(json, "name", self->name);
    }
    if (self->description) {
        fhir_json_add_markdown(json, "description", self->description);
    }
    if (self->part_of) {
        fhir_json_add_reference(json, "partOf", self->part_of);
    }
    
    // Add arrays
    if (self->type && self->type_count > 0) {
        fhir_json_add_codeableconcept_array(json, "type", self->type, self->type_count);
    }
    if (self->alias && self->alias_count > 0) {
        fhir_json_add_string_array(json, "alias", self->alias, self->alias_count);
    }
    if (self->contact && self->contact_count > 0) {
        fhir_json_add_extendedcontactdetail_array(json, "contact", self->contact, self->contact_count);
    }
    if (self->endpoint && self->endpoint_count > 0) {
        fhir_json_add_reference_array(json, "endpoint", self->endpoint, self->endpoint_count);
    }
    
    return json;
}

bool fhir_organization_from_json(FHIROrganization* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "Organization") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse Organization-specific fields
    const cJSON* active_json = cJSON_GetObjectItem(json, "active");
    if (active_json) {
        self->active = fhir_json_parse_boolean(active_json);
    }
    
    const cJSON* name_json = cJSON_GetObjectItem(json, "name");
    if (name_json) {
        self->name = fhir_json_parse_string(name_json);
    }
    
    const cJSON* description_json = cJSON_GetObjectItem(json, "description");
    if (description_json) {
        self->description = fhir_json_parse_markdown(description_json);
    }
    
    const cJSON* part_of_json = cJSON_GetObjectItem(json, "partOf");
    if (part_of_json) {
        self->part_of = fhir_json_parse_reference(part_of_json);
    }
    
    // Parse arrays
    const cJSON* type_json = cJSON_GetObjectItem(json, "type");
    if (type_json && cJSON_IsArray(type_json)) {
        self->type = fhir_json_parse_codeableconcept_array(type_json, &self->type_count);
    }
    
    const cJSON* alias_json = cJSON_GetObjectItem(json, "alias");
    if (alias_json && cJSON_IsArray(alias_json)) {
        self->alias = fhir_json_parse_string_array(alias_json, &self->alias_count);
    }
    
    const cJSON* contact_json = cJSON_GetObjectItem(json, "contact");
    if (contact_json && cJSON_IsArray(contact_json)) {
        self->contact = fhir_json_parse_extendedcontactdetail_array(contact_json, &self->contact_count);
    }
    
    return true;
}

FHIROrganization* fhir_organization_parse(const char* json_string) {
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
    
    FHIROrganization* organization = fhir_organization_create(id);
    if (!organization) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_organization_from_json(organization, json)) {
        fhir_organization_destroy(organization);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return organization;
}

/* ========================================================================== */
/* Organization Validation Methods                                        */
/* ========================================================================== */

bool fhir_organization_validate(const FHIROrganization* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("Organization", self->base.id)) {
        return false;
    }
    
    // Organization has no required fields beyond base resource
    return true;
}

/* ========================================================================== */
/* Organization-Specific Methods                                          */
/* ========================================================================== */

bool fhir_organization_is_active(const FHIROrganization* self) {
    if (!self || !self->active) return false;
    return self->active->value;
}

const char* fhir_organization_get_display_name(const FHIROrganization* self) {
    if (!self) return NULL;
    
    // Return organization name if available
    if (self->name && self->name->value) {
        return self->name->value;
    }
    
    return "Organization";
}

bool fhir_organization_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_ORGANIZATION,
        .name = "Organization",
        .vtable = &Organization_vtable,
        .factory = (FHIRResourceFactory)fhir_organization_create
    };
    
    return fhir_resource_register_type(&registration);
}