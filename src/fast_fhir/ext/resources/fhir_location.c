/**
 * @file fhir_location.c
 * @brief FHIR R5 Location resource C implementation with OOP principles
 * @version 0.1.0
 * @date 2024-01-01
 */

#include "fhir_location.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT(Location, location)

/* ========================================================================== */
/* Location Factory and Lifecycle Methods                             */
/* ========================================================================== */

FHIRLocation* fhir_location_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRLocation* location = fhir_calloc(1, sizeof(FHIRLocation));
    if (!location) {
        return NULL;
    }
    
    if (!fhir_resource_base_init(&location->base, &Location_vtable, 
                                FHIR_RESOURCE_TYPE_LOCATION, id)) {
        fhir_free(location);
        return NULL;
    }
    
    // Initialize Location-specific defaults
    location->status = FHIRLOCATIONSTATUS_ACTIVE;
    location->mode = FHIRLOCATIONMODE_INSTANCE;
    
    return location;
}

void fhir_location_destroy(FHIRLocation* self) {
    if (!self) return;
    
    // Free Location-specific fields
    if (self->operational_status) fhir_coding_destroy(self->operational_status);
    if (self->name) fhir_string_destroy(self->name);
    if (self->description) fhir_markdown_destroy(self->description);
    if (self->address) fhir_address_destroy(self->address);
    if (self->physical_type) fhir_codeableconcept_destroy(self->physical_type);
    if (self->position) fhir_locationposition_destroy(self->position);
    if (self->managing_organization) fhir_reference_destroy(self->managing_organization);
    if (self->part_of) fhir_reference_destroy(self->part_of);
    
    // Free arrays
    fhir_array_destroy((void**)self->alias, self->alias_count, (FHIRDestroyFunc)fhir_string_destroy);
    fhir_array_destroy((void**)self->type, self->type_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->contact, self->contact_count, (FHIRDestroyFunc)fhir_extendedcontactdetail_destroy);
    fhir_array_destroy((void**)self->characteristic, self->characteristic_count, (FHIRDestroyFunc)fhir_codeableconcept_destroy);
    fhir_array_destroy((void**)self->hours_of_operation, self->hours_of_operation_count, (FHIRDestroyFunc)fhir_availability_destroy);
    fhir_array_destroy((void**)self->virtual_service, self->virtual_service_count, (FHIRDestroyFunc)fhir_virtualservicedetail_destroy);
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}

FHIRLocation* fhir_location_clone(const FHIRLocation* self) {
    if (!self) return NULL;
    
    FHIRLocation* clone = fhir_location_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone Location-specific fields
    clone->status = self->status;
    clone->mode = self->mode;
    
    if (self->operational_status) {
        clone->operational_status = fhir_coding_clone(self->operational_status);
    }
    if (self->name) {
        clone->name = fhir_string_clone(self->name);
    }
    if (self->description) {
        clone->description = fhir_markdown_clone(self->description);
    }
    if (self->address) {
        clone->address = fhir_address_clone(self->address);
    }
    if (self->physical_type) {
        clone->physical_type = fhir_codeableconcept_clone(self->physical_type);
    }
    if (self->position) {
        clone->position = fhir_locationposition_clone(self->position);
    }
    if (self->managing_organization) {
        clone->managing_organization = fhir_reference_clone(self->managing_organization);
    }
    if (self->part_of) {
        clone->part_of = fhir_reference_clone(self->part_of);
    }
    
    // Clone arrays
    clone->alias = fhir_array_clone((void**)self->alias, self->alias_count, 
                                   (FHIRCloneFunc)fhir_string_clone, &clone->alias_count);
    clone->type = fhir_array_clone((void**)self->type, self->type_count, 
                                  (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->type_count);
    clone->contact = fhir_array_clone((void**)self->contact, self->contact_count, 
                                     (FHIRCloneFunc)fhir_extendedcontactdetail_clone, &clone->contact_count);
    clone->characteristic = fhir_array_clone((void**)self->characteristic, self->characteristic_count, 
                                            (FHIRCloneFunc)fhir_codeableconcept_clone, &clone->characteristic_count);
    
    return clone;
}

/* ========================================================================== */
/* Location Serialization Methods                                     */
/* ========================================================================== */

cJSON* fhir_location_to_json(const FHIRLocation* self) {
    if (!self) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Location is NULL");
        return NULL;
    }
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "Location") ||
        !fhir_json_add_string(json, "id", self->base.id)) {
        cJSON_Delete(json);
        return NULL;
    }
    
    // Add Location-specific fields
    const char* status_str = (self->status == FHIRLOCATIONSTATUS_ACTIVE) ? "active" :
                            (self->status == FHIRLOCATIONSTATUS_SUSPENDED) ? "suspended" : "inactive";
    fhir_json_add_string(json, "status", status_str);
    
    const char* mode_str = (self->mode == FHIRLOCATIONMODE_INSTANCE) ? "instance" : "kind";
    fhir_json_add_string(json, "mode", mode_str);
    
    if (self->operational_status) {
        fhir_json_add_coding(json, "operationalStatus", self->operational_status);
    }
    if (self->name) {
        fhir_json_add_string_value(json, "name", self->name);
    }
    if (self->description) {
        fhir_json_add_markdown(json, "description", self->description);
    }
    if (self->address) {
        fhir_json_add_address(json, "address", self->address);
    }
    if (self->physical_type) {
        fhir_json_add_codeableconcept(json, "physicalType", self->physical_type);
    }
    if (self->position) {
        fhir_json_add_locationposition(json, "position", self->position);
    }
    if (self->managing_organization) {
        fhir_json_add_reference(json, "managingOrganization", self->managing_organization);
    }
    if (self->part_of) {
        fhir_json_add_reference(json, "partOf", self->part_of);
    }
    
    // Add arrays
    if (self->alias && self->alias_count > 0) {
        fhir_json_add_string_array(json, "alias", self->alias, self->alias_count);
    }
    if (self->type && self->type_count > 0) {
        fhir_json_add_codeableconcept_array(json, "type", self->type, self->type_count);
    }
    if (self->contact && self->contact_count > 0) {
        fhir_json_add_extendedcontactdetail_array(json, "contact", self->contact, self->contact_count);
    }
    if (self->characteristic && self->characteristic_count > 0) {
        fhir_json_add_codeableconcept_array(json, "characteristic", self->characteristic, self->characteristic_count);
    }
    
    return json;
}

bool fhir_location_from_json(FHIRLocation* self, const cJSON* json) {
    if (!self || !json) {
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "Location") != 0) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }
    
    // Parse Location-specific fields
    const char* status_str = fhir_json_get_string(json, "status");
    if (status_str) {
        if (strcmp(status_str, "active") == 0) {
            self->status = FHIRLOCATIONSTATUS_ACTIVE;
        } else if (strcmp(status_str, "suspended") == 0) {
            self->status = FHIRLOCATIONSTATUS_SUSPENDED;
        } else if (strcmp(status_str, "inactive") == 0) {
            self->status = FHIRLOCATIONSTATUS_INACTIVE;
        }
    }
    
    const char* mode_str = fhir_json_get_string(json, "mode");
    if (mode_str) {
        if (strcmp(mode_str, "instance") == 0) {
            self->mode = FHIRLOCATIONMODE_INSTANCE;
        } else if (strcmp(mode_str, "kind") == 0) {
            self->mode = FHIRLOCATIONMODE_KIND;
        }
    }
    
    const cJSON* operational_status_json = cJSON_GetObjectItem(json, "operationalStatus");
    if (operational_status_json) {
        self->operational_status = fhir_json_parse_coding(operational_status_json);
    }
    
    const cJSON* name_json = cJSON_GetObjectItem(json, "name");
    if (name_json) {
        self->name = fhir_json_parse_string(name_json);
    }
    
    const cJSON* description_json = cJSON_GetObjectItem(json, "description");
    if (description_json) {
        self->description = fhir_json_parse_markdown(description_json);
    }
    
    const cJSON* address_json = cJSON_GetObjectItem(json, "address");
    if (address_json) {
        self->address = fhir_json_parse_address(address_json);
    }
    
    const cJSON* physical_type_json = cJSON_GetObjectItem(json, "physicalType");
    if (physical_type_json) {
        self->physical_type = fhir_json_parse_codeableconcept(physical_type_json);
    }
    
    const cJSON* managing_organization_json = cJSON_GetObjectItem(json, "managingOrganization");
    if (managing_organization_json) {
        self->managing_organization = fhir_json_parse_reference(managing_organization_json);
    }
    
    const cJSON* part_of_json = cJSON_GetObjectItem(json, "partOf");
    if (part_of_json) {
        self->part_of = fhir_json_parse_reference(part_of_json);
    }
    
    // Parse arrays
    const cJSON* alias_json = cJSON_GetObjectItem(json, "alias");
    if (alias_json && cJSON_IsArray(alias_json)) {
        self->alias = fhir_json_parse_string_array(alias_json, &self->alias_count);
    }
    
    const cJSON* type_json = cJSON_GetObjectItem(json, "type");
    if (type_json && cJSON_IsArray(type_json)) {
        self->type = fhir_json_parse_codeableconcept_array(type_json, &self->type_count);
    }
    
    return true;
}

FHIRLocation* fhir_location_parse(const char* json_string) {
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
    
    FHIRLocation* location = fhir_location_create(id);
    if (!location) {
        cJSON_Delete(json);
        return NULL;
    }
    
    if (!fhir_location_from_json(location, json)) {
        fhir_location_destroy(location);
        cJSON_Delete(json);
        return NULL;
    }
    
    cJSON_Delete(json);
    return location;
}

/* ========================================================================== */
/* Location Validation Methods                                        */
/* ========================================================================== */

bool fhir_location_validate(const FHIRLocation* self) {
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("Location", self->base.id)) {
        return false;
    }
    
    // Location has no required fields beyond base resource
    return true;
}

/* ========================================================================== */
/* Location-Specific Methods                                          */
/* ========================================================================== */

bool fhir_location_is_active(const FHIRLocation* self) {
    if (!self) return false;
    return self->status == FHIRLOCATIONSTATUS_ACTIVE;
}

const char* fhir_location_get_display_name(const FHIRLocation* self) {
    if (!self) return NULL;
    
    // Return location name if available
    if (self->name && self->name->value) {
        return self->name->value;
    }
    
    return "Location";
}

bool fhir_location_register(void) {
    FHIRResourceRegistration registration = {
        .type = FHIR_RESOURCE_TYPE_LOCATION,
        .name = "Location",
        .vtable = &Location_vtable,
        .factory = (FHIRResourceFactory)fhir_location_create
    };
    
    return fhir_resource_register_type(&registration);
}