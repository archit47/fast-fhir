#!/usr/bin/env python3
"""
Resource Generator for FHIR C Extensions
Automatically generates C header and implementation files for FHIR resources
following OOP principles and best practices.
"""

import os
import re
from typing import Dict, List, Tuple

# Resource definitions with their key fields and characteristics
RESOURCES = {
    "PractitionerRole": {
        "category": "foundation",
        "description": "A specific set of Roles/Locations/specialties/services that a practitioner may perform",
        "key_fields": [
            ("active", "FHIRBoolean*", "Whether this practitioner role record is in active use"),
            ("period", "FHIRPeriod*", "The period during which the practitioner is authorized to perform in these role(s)"),
            ("practitioner", "FHIRReference*", "Practitioner that is able to provide the defined services"),
            ("organization", "FHIRReference*", "Organization where the roles are available"),
            ("code", "FHIRCodeableConcept**", "Roles which this practitioner is authorized to perform"),
            ("specialty", "FHIRCodeableConcept**", "Specific specialty of the practitioner"),
            ("location", "FHIRReference**", "The location(s) at which this practitioner provides care"),
            ("healthcare_service", "FHIRReference**", "The list of healthcare services that this worker provides"),
            ("contact", "FHIRExtendedContactDetail**", "Official contact details relating to this PractitionerRole"),
            ("characteristic", "FHIRCodeableConcept**", "Collection of characteristics (attributes)"),
            ("communication", "FHIRCodeableConcept**", "A language the practitioner can use in patient communication"),
            ("availability", "FHIRAvailability**", "Times the practitioner is available or performing this role"),
            ("endpoint", "FHIRReference**", "Technical endpoints providing access to services operated for the practitioner")
        ],
        "enums": [
            ("active_status", ["active", "inactive"])
        ],
        "required_fields": ["practitioner", "organization"],
        "choice_types": [],
        "arrays": ["code", "specialty", "location", "healthcare_service", "contact", "characteristic", "communication", "availability", "endpoint"]
    },
    
    "Organization": {
        "category": "foundation", 
        "description": "A formally or informally recognized grouping of people or organizations",
        "key_fields": [
            ("active", "FHIRBoolean*", "Whether the organization's record is still in active use"),
            ("type", "FHIRCodeableConcept**", "Kind of organization"),
            ("name", "FHIRString*", "Name used for the organization"),
            ("alias", "FHIRString**", "A list of alternate names that the organization is known as"),
            ("description", "FHIRMarkdown*", "Additional details about the organization"),
            ("contact", "FHIRExtendedContactDetail**", "Official contact details for the organization"),
            ("part_of", "FHIRReference*", "The organization of which this organization forms a part"),
            ("endpoint", "FHIRReference**", "Technical endpoints providing access to services operated for the organization"),
            ("qualification", "FHIROrganizationQualification**", "Qualifications, certifications, accreditations, licenses, training, etc.")
        ],
        "enums": [],
        "required_fields": [],
        "choice_types": [],
        "arrays": ["type", "alias", "contact", "endpoint", "qualification"]
    },
    
    "Location": {
        "category": "foundation",
        "description": "Details and position information for a physical place",
        "key_fields": [
            ("status", "FHIRLocationStatus", "active | suspended | inactive"),
            ("operational_status", "FHIRCoding*", "The operational status covers operation values most relevant to beds"),
            ("name", "FHIRString*", "Name of the location as used by humans"),
            ("alias", "FHIRString**", "A list of alternate names that the location is known as"),
            ("description", "FHIRMarkdown*", "Additional details about the location"),
            ("mode", "FHIRLocationMode", "instance | kind"),
            ("type", "FHIRCodeableConcept**", "Type of function performed"),
            ("contact", "FHIRExtendedContactDetail**", "Official contact details for the location"),
            ("address", "FHIRAddress*", "Physical location"),
            ("physical_type", "FHIRCodeableConcept*", "Physical form of the location"),
            ("position", "FHIRLocationPosition*", "The absolute geographic location"),
            ("managing_organization", "FHIRReference*", "Organization responsible for provisioning and upkeep"),
            ("part_of", "FHIRReference*", "Another Location this one is physically a part of"),
            ("characteristic", "FHIRCodeableConcept**", "Collection of characteristics (attributes)"),
            ("hours_of_operation", "FHIRAvailability**", "What days/times during a week is this location usually open"),
            ("virtual_service", "FHIRVirtualServiceDetail**", "Connection details of a virtual service")
        ],
        "enums": [
            ("status", ["active", "suspended", "inactive"]),
            ("mode", ["instance", "kind"])
        ],
        "required_fields": [],
        "choice_types": [],
        "arrays": ["alias", "type", "contact", "characteristic", "hours_of_operation", "virtual_service"]
    }
}

def generate_header_file(resource_name: str, resource_info: Dict) -> str:
    """Generate C header file for a resource."""
    
    header_guard = f"FHIR_{resource_name.upper()}_H"
    
    header = f'''/**
 * @file fhir_{resource_name.lower()}.h
 * @brief FHIR R5 {resource_name} resource C interface with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 * 
 * {resource_info["description"]}
 */

#ifndef {header_guard}
#define {header_guard}

#include "../common/fhir_resource_base.h"
#include "../fhir_datatypes.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {{
#endif

'''
    
    # Add enumerations
    for enum_name, values in resource_info.get("enums", []):
        enum_type = f"FHIR{resource_name}{enum_name.title().replace('_', '')}"
        header += f'''/**
 * @brief {resource_name} {enum_name} enumeration
 */
typedef enum {{
'''
        for i, value in enumerate(values):
            header += f'    {enum_type.upper()}_{value.upper().replace("-", "_")} = {i},\n'
        header += f'}} {enum_type};\n\n'
    
    # Add resource structure
    header += f'''/**
 * @brief FHIR R5 {resource_name} resource structure
 * 
 * {resource_info["description"]}
 */
FHIR_RESOURCE_DEFINE({resource_name})
    // {resource_name}-specific fields
'''
    
    for field_name, field_type, description in resource_info["key_fields"]:
        if field_name in resource_info.get("arrays", []):
            header += f'    {field_type} {field_name};\n'
            header += f'    size_t {field_name}_count;\n'
        else:
            header += f'    {field_type} {field_name};\n'
        header += f'    \n'
    
    header += '};\n\n'
    
    # Add function declarations
    header += f'''/* ========================================================================== */
/* {resource_name} Factory and Lifecycle Methods                             */
/* ========================================================================== */

/**
 * @brief Create a new {resource_name} resource
 * @param id Resource identifier (required)
 * @return Pointer to new {resource_name} or NULL on failure
 */
FHIR{resource_name}* fhir_{resource_name.lower()}_create(const char* id);

/**
 * @brief Destroy {resource_name} resource (virtual destructor)
 * @param self {resource_name} to destroy
 */
void fhir_{resource_name.lower()}_destroy(FHIR{resource_name}* self);

/**
 * @brief Clone {resource_name} resource (virtual clone)
 * @param self {resource_name} to clone
 * @return Cloned {resource_name} or NULL on failure
 */
FHIR{resource_name}* fhir_{resource_name.lower()}_clone(const FHIR{resource_name}* self);

/* ========================================================================== */
/* {resource_name} Serialization Methods                                     */
/* ========================================================================== */

/**
 * @brief Convert {resource_name} to JSON (virtual method)
 * @param self {resource_name} to convert
 * @return JSON object or NULL on failure
 */
cJSON* fhir_{resource_name.lower()}_to_json(const FHIR{resource_name}* self);

/**
 * @brief Load {resource_name} from JSON (virtual method)
 * @param self {resource_name} to populate
 * @param json JSON object
 * @return true on success, false on failure
 */
bool fhir_{resource_name.lower()}_from_json(FHIR{resource_name}* self, const cJSON* json);

/**
 * @brief Parse {resource_name} from JSON string
 * @param json_string JSON string
 * @return New {resource_name} or NULL on failure
 */
FHIR{resource_name}* fhir_{resource_name.lower()}_parse(const char* json_string);

/* ========================================================================== */
/* {resource_name} Validation Methods                                        */
/* ========================================================================== */

/**
 * @brief Validate {resource_name} resource (virtual method)
 * @param self {resource_name} to validate
 * @return true if valid, false otherwise
 */
bool fhir_{resource_name.lower()}_validate(const FHIR{resource_name}* self);

/* ========================================================================== */
/* {resource_name}-Specific Methods                                          */
/* ========================================================================== */

/**
 * @brief Check if {resource_name} is active (virtual method)
 * @param self {resource_name} to check
 * @return true if active, false otherwise
 */
bool fhir_{resource_name.lower()}_is_active(const FHIR{resource_name}* self);

/**
 * @brief Get {resource_name} display name (virtual method)
 * @param self {resource_name} to get name from
 * @return Display name or NULL
 */
const char* fhir_{resource_name.lower()}_get_display_name(const FHIR{resource_name}* self);

/**
 * @brief Register {resource_name} resource type
 * @return true on success, false on failure
 */
bool fhir_{resource_name.lower()}_register(void);

#ifdef __cplusplus
}}
#endif

#endif /* {header_guard} */'''
    
    return header

def generate_implementation_file(resource_name: str, resource_info: Dict) -> str:
    """Generate C implementation file for a resource."""
    
    impl = f'''/**
 * @file fhir_{resource_name.lower()}.c
 * @brief FHIR R5 {resource_name} resource C implementation with OOP principles
 * @version 1.0.0
 * @date 2024-01-01
 */

#include "fhir_{resource_name.lower()}.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ========================================================================== */
/* Virtual Function Table                                                     */
/* ========================================================================== */

FHIR_RESOURCE_VTABLE_INIT({resource_name}, {resource_name.lower()})

/* ========================================================================== */
/* {resource_name} Factory and Lifecycle Methods                             */
/* ========================================================================== */

FHIR{resource_name}* fhir_{resource_name.lower()}_create(const char* id) {{
    if (!fhir_validate_id(id)) {{
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, "Invalid ID format", "id");
        return NULL;
    }}
    
    FHIR{resource_name}* {resource_name.lower()} = fhir_calloc(1, sizeof(FHIR{resource_name}));
    if (!{resource_name.lower()}) {{
        return NULL;
    }}
    
    if (!fhir_resource_base_init(&{resource_name.lower()}->base, &{resource_name}_vtable, 
                                FHIR_RESOURCE_TYPE_{resource_name.upper()}, id)) {{
        fhir_free({resource_name.lower()});
        return NULL;
    }}
    
    // Initialize {resource_name}-specific defaults
    // Add default initialization here
    
    return {resource_name.lower()};
}}

void fhir_{resource_name.lower()}_destroy(FHIR{resource_name}* self) {{
    if (!self) return;
    
    // Free {resource_name}-specific fields
    // Add field cleanup here
    
    // Free base resource
    fhir_resource_base_cleanup(&self->base);
    
    fhir_free(self);
}}

FHIR{resource_name}* fhir_{resource_name.lower()}_clone(const FHIR{resource_name}* self) {{
    if (!self) return NULL;
    
    FHIR{resource_name}* clone = fhir_{resource_name.lower()}_create(self->base.id);
    if (!clone) return NULL;
    
    // Clone {resource_name}-specific fields
    // Add field cloning here
    
    return clone;
}}

/* ========================================================================== */
/* {resource_name} Serialization Methods                                     */
/* ========================================================================== */

cJSON* fhir_{resource_name.lower()}_to_json(const FHIR{resource_name}* self) {{
    if (!self) {{
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "{resource_name} is NULL");
        return NULL;
    }}
    
    cJSON* json = cJSON_CreateObject();
    if (!json) {{
        FHIR_SET_ERROR(FHIR_ERROR_OUT_OF_MEMORY, "Failed to create JSON object");
        return NULL;
    }}
    
    // Add resource type and id
    if (!fhir_json_add_string(json, "resourceType", "{resource_name}") ||
        !fhir_json_add_string(json, "id", self->base.id)) {{
        cJSON_Delete(json);
        return NULL;
    }}
    
    // Add {resource_name}-specific fields
    // Add field serialization here
    
    return json;
}}

bool fhir_{resource_name.lower()}_from_json(FHIR{resource_name}* self, const cJSON* json) {{
    if (!self || !json) {{
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return false;
    }}
    
    // Validate resource type
    const char* resource_type = fhir_json_get_string(json, "resourceType");
    if (!resource_type || strcmp(resource_type, "{resource_name}") != 0) {{
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_INVALID_RESOURCE_TYPE, "Invalid resource type", "resourceType");
        return false;
    }}
    
    // Parse {resource_name}-specific fields
    // Add field parsing here
    
    return true;
}}

FHIR{resource_name}* fhir_{resource_name.lower()}_parse(const char* json_string) {{
    if (!json_string) {{
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_ARGUMENT, "JSON string is NULL");
        return NULL;
    }}
    
    cJSON* json = cJSON_Parse(json_string);
    if (!json) {{
        FHIR_SET_ERROR(FHIR_ERROR_INVALID_JSON, "Failed to parse JSON");
        return NULL;
    }}
    
    const char* id = fhir_json_get_string(json, "id");
    if (!id) {{
        cJSON_Delete(json);
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "id");
        return NULL;
    }}
    
    FHIR{resource_name}* {resource_name.lower()} = fhir_{resource_name.lower()}_create(id);
    if (!{resource_name.lower()}) {{
        cJSON_Delete(json);
        return NULL;
    }}
    
    if (!fhir_{resource_name.lower()}_from_json({resource_name.lower()}, json)) {{
        fhir_{resource_name.lower()}_destroy({resource_name.lower()});
        cJSON_Delete(json);
        return NULL;
    }}
    
    cJSON_Delete(json);
    return {resource_name.lower()};
}}

/* ========================================================================== */
/* {resource_name} Validation Methods                                        */
/* ========================================================================== */

bool fhir_{resource_name.lower()}_validate(const FHIR{resource_name}* self) {{
    if (!self) return false;
    
    // Validate base resource
    if (!fhir_validate_base_resource("{resource_name}", self->base.id)) {{
        return false;
    }}
    
    // Validate required fields
'''
    
    for field in resource_info.get("required_fields", []):
        impl += f'''    if (!self->{field}) {{
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_MISSING_REQUIRED_FIELD, "Missing required field", "{field}");
        return false;
    }}
    
'''
    
    impl += f'''    return true;
}}

/* ========================================================================== */
/* {resource_name}-Specific Methods                                          */
/* ========================================================================== */

bool fhir_{resource_name.lower()}_is_active(const FHIR{resource_name}* self) {{
    if (!self || !self->active) return false;
    return self->active->value;
}}

const char* fhir_{resource_name.lower()}_get_display_name(const FHIR{resource_name}* self) {{
    if (!self) return NULL;
    
    // Return appropriate display name based on resource type
    // Implementation depends on resource-specific fields
    return "{resource_name} Display Name"; // Placeholder
}}

bool fhir_{resource_name.lower()}_register(void) {{
    FHIRResourceRegistration registration = {{
        .type = FHIR_RESOURCE_TYPE_{resource_name.upper()},
        .name = "{resource_name}",
        .vtable = &{resource_name}_vtable,
        .factory = (FHIRResourceFactory)fhir_{resource_name.lower()}_create
    }};
    
    return fhir_resource_register_type(&registration);
}}'''
    
    return impl

def create_resource_files(resource_name: str, resource_info: Dict):
    """Create header and implementation files for a resource."""
    
    # Create directories if they don't exist
    os.makedirs("src/fhir/ext/resources", exist_ok=True)
    
    # Generate header file
    header_content = generate_header_file(resource_name, resource_info)
    header_path = f"src/fhir/ext/resources/fhir_{resource_name.lower()}.h"
    
    with open(header_path, 'w') as f:
        f.write(header_content)
    
    print(f"✓ Created {header_path}")
    
    # Generate implementation file
    impl_content = generate_implementation_file(resource_name, resource_info)
    impl_path = f"src/fhir/ext/resources/fhir_{resource_name.lower()}.c"
    
    with open(impl_path, 'w') as f:
        f.write(impl_content)
    
    print(f"✓ Created {impl_path}")

def main():
    """Generate all resource files."""
    print("=== FHIR Resource Generator ===\n")
    
    for resource_name, resource_info in RESOURCES.items():
        print(f"Generating {resource_name}...")
        create_resource_files(resource_name, resource_info)
        print()
    
    print("🎉 All resource files generated successfully!")
    print("\nNext steps:")
    print("1. Review generated files and customize as needed")
    print("2. Implement resource-specific logic in the placeholder sections")
    print("3. Add comprehensive tests for each resource")
    print("4. Update CMakeLists.txt to include new resources")
    print("5. Build and test the complete system")

if __name__ == "__main__":
    main()