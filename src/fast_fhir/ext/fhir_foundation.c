#include "fhir_foundation.h"
#include <stdlib.h>
#include <string.h>

// Base Resource functions
FHIRResource* fhir_resource_create(const char* resource_type, const char* id) {
    FHIRResource* resource = calloc(1, sizeof(FHIRResource));
    if (resource) {
        resource->resource_type = fhir_string_duplicate(resource_type);
        resource->id = fhir_string_duplicate(id);
    }
    return resource;
}

FHIRDomainResource* fhir_domain_resource_create(const char* resource_type, const char* id) {
    FHIRDomainResource* domain_resource = calloc(1, sizeof(FHIRDomainResource));
    if (domain_resource) {
        domain_resource->resource.resource_type = fhir_string_duplicate(resource_type);
        domain_resource->resource.id = fhir_string_duplicate(id);
    }
    return domain_resource;
}

void fhir_resource_free(FHIRResource* resource) {
    if (resource) {
        fhir_string_free(resource->resource_type);
        fhir_string_free(resource->id);
        if (resource->meta) {
            // Free meta structure
            free(resource->meta);
        }
        if (resource->implicit_rules) {
            fhir_string_free(resource->implicit_rules->value);
            free(resource->implicit_rules);
        }
        if (resource->language) {
            fhir_string_free(resource->language->value);
            free(resource->language);
        }
        free(resource);
    }
}

void fhir_domain_resource_free(FHIRDomainResource* domain_resource) {
    if (domain_resource) {
        fhir_resource_free(&domain_resource->resource);
        
        // Free contained resources
        if (domain_resource->contained) {
            for (size_t i = 0; i < domain_resource->contained_count; i++) {
                fhir_resource_free(domain_resource->contained[i]);
            }
            free(domain_resource->contained);
        }
        
        // Free extensions
        if (domain_resource->extension) {
            for (size_t i = 0; i < domain_resource->extension_count; i++) {
                free(domain_resource->extension[i]);
            }
            free(domain_resource->extension);
        }
        
        if (domain_resource->modifier_extension) {
            for (size_t i = 0; i < domain_resource->modifier_extension_count; i++) {
                free(domain_resource->modifier_extension[i]);
            }
            free(domain_resource->modifier_extension);
        }
        
        free(domain_resource);
    }
}

// Patient Resource functions
FHIRPatient* fhir_patient_create(const char* id) {
    FHIRPatient* patient = calloc(1, sizeof(FHIRPatient));
    if (patient) {
        patient->domain_resource.resource.resource_type = fhir_string_duplicate("Patient");
        patient->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return patient;
}

void fhir_patient_free(FHIRPatient* patient) {
    if (patient) {
        fhir_domain_resource_free(&patient->domain_resource);
        
        // Free identifiers
        if (patient->identifier) {
            for (size_t i = 0; i < patient->identifier_count; i++) {
                // Free identifier structure
                free(patient->identifier[i]);
            }
            free(patient->identifier);
        }
        
        // Free names
        if (patient->name) {
            for (size_t i = 0; i < patient->name_count; i++) {
                // Free human name structure
                free(patient->name[i]);
            }
            free(patient->name);
        }
        
        // Free telecom
        if (patient->telecom) {
            for (size_t i = 0; i < patient->telecom_count; i++) {
                free(patient->telecom[i]);
            }
            free(patient->telecom);
        }
        
        // Free addresses
        if (patient->address) {
            for (size_t i = 0; i < patient->address_count; i++) {
                free(patient->address[i]);
            }
            free(patient->address);
        }
        
        // Free other fields
        if (patient->active) free(patient->active);
        if (patient->gender) {
            fhir_string_free(patient->gender->value);
            free(patient->gender);
        }
        if (patient->birth_date) {
            fhir_string_free(patient->birth_date->value);
            free(patient->birth_date);
        }
        if (patient->deceased_boolean) free(patient->deceased_boolean);
        if (patient->deceased_date_time) {
            fhir_string_free(patient->deceased_date_time->value);
            free(patient->deceased_date_time);
        }
        if (patient->marital_status) free(patient->marital_status);
        if (patient->multiple_birth_boolean) free(patient->multiple_birth_boolean);
        if (patient->multiple_birth_integer) free(patient->multiple_birth_integer);
        
        // Free photos
        if (patient->photo) {
            for (size_t i = 0; i < patient->photo_count; i++) {
                free(patient->photo[i]);
            }
            free(patient->photo);
        }
        
        // Free contacts
        if (patient->contact) {
            for (size_t i = 0; i < patient->contact_count; i++) {
                free(patient->contact[i]);
            }
            free(patient->contact);
        }
        
        // Free communications
        if (patient->communication) {
            for (size_t i = 0; i < patient->communication_count; i++) {
                free(patient->communication[i]);
            }
            free(patient->communication);
        }
        
        // Free general practitioners
        if (patient->general_practitioner) {
            for (size_t i = 0; i < patient->general_practitioner_count; i++) {
                free(patient->general_practitioner[i]);
            }
            free(patient->general_practitioner);
        }
        
        if (patient->managing_organization) free(patient->managing_organization);
        
        // Free links
        if (patient->link) {
            for (size_t i = 0; i < patient->link_count; i++) {
                free(patient->link[i]);
            }
            free(patient->link);
        }
        
        free(patient);
    }
}

FHIRPatient* fhir_parse_patient(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) return NULL;
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || strcmp(resource_type->valuestring, "Patient") != 0) {
        return NULL;
    }
    
    cJSON* id = cJSON_GetObjectItemCaseSensitive(json, "id");
    const char* id_str = cJSON_IsString(id) ? id->valuestring : NULL;
    
    FHIRPatient* patient = fhir_patient_create(id_str);
    if (!patient) return NULL;
    
    // Parse active
    cJSON* active = cJSON_GetObjectItemCaseSensitive(json, "active");
    if (cJSON_IsBool(active)) {
        patient->active = fhir_boolean_create(cJSON_IsTrue(active));
    }
    
    // Parse gender
    cJSON* gender = cJSON_GetObjectItemCaseSensitive(json, "gender");
    if (cJSON_IsString(gender)) {
        patient->gender = calloc(1, sizeof(FHIRCode));
        if (patient->gender) {
            patient->gender->value = fhir_string_duplicate(gender->valuestring);
        }
    }
    
    // Parse birthDate
    cJSON* birth_date = cJSON_GetObjectItemCaseSensitive(json, "birthDate");
    if (cJSON_IsString(birth_date)) {
        patient->birth_date = calloc(1, sizeof(FHIRDate));
        if (patient->birth_date) {
            patient->birth_date->value = fhir_string_duplicate(birth_date->valuestring);
        }
    }
    
    // Parse name array
    cJSON* name_array = cJSON_GetObjectItemCaseSensitive(json, "name");
    if (cJSON_IsArray(name_array)) {
        int array_size = cJSON_GetArraySize(name_array);
        if (array_size > 0) {
            patient->name = calloc(array_size, sizeof(FHIRHumanName*));
            patient->name_count = 0;
            
            cJSON* name_item = NULL;
            cJSON_ArrayForEach(name_item, name_array) {
                FHIRHumanName* human_name = fhir_parse_human_name(name_item);
                if (human_name) {
                    patient->name[patient->name_count++] = human_name;
                }
            }
        }
    }
    
    // Parse identifier array
    cJSON* identifier_array = cJSON_GetObjectItemCaseSensitive(json, "identifier");
    if (cJSON_IsArray(identifier_array)) {
        int array_size = cJSON_GetArraySize(identifier_array);
        if (array_size > 0) {
            patient->identifier = calloc(array_size, sizeof(FHIRIdentifier*));
            patient->identifier_count = 0;
            
            cJSON* identifier_item = NULL;
            cJSON_ArrayForEach(identifier_item, identifier_array) {
                FHIRIdentifier* identifier = fhir_parse_identifier(identifier_item);
                if (identifier) {
                    patient->identifier[patient->identifier_count++] = identifier;
                }
            }
        }
    }
    
    // Parse telecom array
    cJSON* telecom_array = cJSON_GetObjectItemCaseSensitive(json, "telecom");
    if (cJSON_IsArray(telecom_array)) {
        int array_size = cJSON_GetArraySize(telecom_array);
        if (array_size > 0) {
            patient->telecom = calloc(array_size, sizeof(FHIRContactPoint*));
            patient->telecom_count = 0;
            
            cJSON* telecom_item = NULL;
            cJSON_ArrayForEach(telecom_item, telecom_array) {
                FHIRContactPoint* contact_point = fhir_parse_contact_point(telecom_item);
                if (contact_point) {
                    patient->telecom[patient->telecom_count++] = contact_point;
                }
            }
        }
    }
    
    // Parse address array
    cJSON* address_array = cJSON_GetObjectItemCaseSensitive(json, "address");
    if (cJSON_IsArray(address_array)) {
        int array_size = cJSON_GetArraySize(address_array);
        if (array_size > 0) {
            patient->address = calloc(array_size, sizeof(FHIRAddress*));
            patient->address_count = 0;
            
            cJSON* address_item = NULL;
            cJSON_ArrayForEach(address_item, address_array) {
                FHIRAddress* address = fhir_parse_address(address_item);
                if (address) {
                    patient->address[patient->address_count++] = address;
                }
            }
        }
    }
    
    return patient;
}

cJSON* fhir_patient_to_json(const FHIRPatient* patient) {
    if (!patient) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    // Add resourceType
    cJSON_AddStringToObject(json, "resourceType", "Patient");
    
    // Add id
    if (patient->domain_resource.resource.id) {
        cJSON_AddStringToObject(json, "id", patient->domain_resource.resource.id);
    }
    
    // Add active
    if (patient->active) {
        cJSON_AddBoolToObject(json, "active", patient->active->value);
    }
    
    // Add gender
    if (patient->gender && patient->gender->value) {
        cJSON_AddStringToObject(json, "gender", patient->gender->value);
    }
    
    // Add birthDate
    if (patient->birth_date && patient->birth_date->value) {
        cJSON_AddStringToObject(json, "birthDate", patient->birth_date->value);
    }
    
    // Add name array
    if (patient->name && patient->name_count > 0) {
        cJSON* name_array = cJSON_CreateArray();
        for (size_t i = 0; i < patient->name_count; i++) {
            cJSON* name_json = fhir_human_name_to_json(patient->name[i]);
            if (name_json) {
                cJSON_AddItemToArray(name_array, name_json);
            }
        }
        cJSON_AddItemToObject(json, "name", name_array);
    }
    
    // Add identifier array
    if (patient->identifier && patient->identifier_count > 0) {
        cJSON* identifier_array = cJSON_CreateArray();
        for (size_t i = 0; i < patient->identifier_count; i++) {
            cJSON* identifier_json = fhir_identifier_to_json(patient->identifier[i]);
            if (identifier_json) {
                cJSON_AddItemToArray(identifier_array, identifier_json);
            }
        }
        cJSON_AddItemToObject(json, "identifier", identifier_array);
    }
    
    // Add telecom array
    if (patient->telecom && patient->telecom_count > 0) {
        cJSON* telecom_array = cJSON_CreateArray();
        for (size_t i = 0; i < patient->telecom_count; i++) {
            cJSON* telecom_json = fhir_contact_point_to_json(patient->telecom[i]);
            if (telecom_json) {
                cJSON_AddItemToArray(telecom_array, telecom_json);
            }
        }
        cJSON_AddItemToObject(json, "telecom", telecom_array);
    }
    
    // Add address array
    if (patient->address && patient->address_count > 0) {
        cJSON* address_array = cJSON_CreateArray();
        for (size_t i = 0; i < patient->address_count; i++) {
            cJSON* address_json = fhir_address_to_json(patient->address[i]);
            if (address_json) {
                cJSON_AddItemToArray(address_array, address_json);
            }
        }
        cJSON_AddItemToObject(json, "address", address_array);
    }
    
    return json;
}

// Practitioner Resource functions
FHIRPractitioner* fhir_practitioner_create(const char* id) {
    FHIRPractitioner* practitioner = calloc(1, sizeof(FHIRPractitioner));
    if (practitioner) {
        practitioner->domain_resource.resource.resource_type = fhir_string_duplicate("Practitioner");
        practitioner->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return practitioner;
}

void fhir_practitioner_free(FHIRPractitioner* practitioner) {
    if (practitioner) {
        fhir_domain_resource_free(&practitioner->domain_resource);
        
        // Free identifiers
        if (practitioner->identifier) {
            for (size_t i = 0; i < practitioner->identifier_count; i++) {
                free(practitioner->identifier[i]);
            }
            free(practitioner->identifier);
        }
        
        // Free names
        if (practitioner->name) {
            for (size_t i = 0; i < practitioner->name_count; i++) {
                free(practitioner->name[i]);
            }
            free(practitioner->name);
        }
        
        // Free other fields
        if (practitioner->active) free(practitioner->active);
        if (practitioner->gender) {
            fhir_string_free(practitioner->gender->value);
            free(practitioner->gender);
        }
        if (practitioner->birth_date) {
            fhir_string_free(practitioner->birth_date->value);
            free(practitioner->birth_date);
        }
        
        // Free qualifications
        if (practitioner->qualification) {
            for (size_t i = 0; i < practitioner->qualification_count; i++) {
                free(practitioner->qualification[i]);
            }
            free(practitioner->qualification);
        }
        
        free(practitioner);
    }
}

// Organization Resource functions
FHIROrganization* fhir_organization_create(const char* id) {
    FHIROrganization* organization = calloc(1, sizeof(FHIROrganization));
    if (organization) {
        organization->domain_resource.resource.resource_type = fhir_string_duplicate("Organization");
        organization->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return organization;
}

void fhir_organization_free(FHIROrganization* organization) {
    if (organization) {
        fhir_domain_resource_free(&organization->domain_resource);
        
        // Free identifiers
        if (organization->identifier) {
            for (size_t i = 0; i < organization->identifier_count; i++) {
                free(organization->identifier[i]);
            }
            free(organization->identifier);
        }
        
        // Free other fields
        if (organization->active) free(organization->active);
        if (organization->name) {
            fhir_string_free(organization->name->value);
            free(organization->name);
        }
        if (organization->description) {
            fhir_string_free(organization->description->value);
            free(organization->description);
        }
        
        // Free aliases
        if (organization->alias) {
            for (size_t i = 0; i < organization->alias_count; i++) {
                if (organization->alias[i]) {
                    fhir_string_free(organization->alias[i]->value);
                    free(organization->alias[i]);
                }
            }
            free(organization->alias);
        }
        
        free(organization);
    }
}

// Utility functions
char* fhir_patient_get_full_name(const FHIRPatient* patient) {
    if (!patient || !patient->name || patient->name_count == 0) {
        return NULL;
    }
    
    FHIRHumanName* first_name = patient->name[0];
    if (!first_name) return NULL;
    
    // Check if text field is available
    if (first_name->text) {
        return fhir_string_duplicate(first_name->text);
    }
    
    // Construct name from parts
    size_t total_length = 0;
    
    // Calculate total length needed
    if (first_name->given) {
        for (size_t i = 0; i < first_name->given_count; i++) {
            if (first_name->given[i]) {
                total_length += strlen(first_name->given[i]) + 1; // +1 for space
            }
        }
    }
    
    if (first_name->family) {
        for (size_t i = 0; i < first_name->family_count; i++) {
            if (first_name->family[i]) {
                total_length += strlen(first_name->family[i]) + 1; // +1 for space
            }
        }
    }
    
    if (total_length == 0) return NULL;
    
    char* full_name = malloc(total_length + 1);
    if (!full_name) return NULL;
    
    full_name[0] = '\0';
    
    // Add given names
    if (first_name->given) {
        for (size_t i = 0; i < first_name->given_count; i++) {
            if (first_name->given[i]) {
                if (strlen(full_name) > 0) {
                    strcat(full_name, " ");
                }
                strcat(full_name, first_name->given[i]);
            }
        }
    }
    
    // Add family names
    if (first_name->family) {
        for (size_t i = 0; i < first_name->family_count; i++) {
            if (first_name->family[i]) {
                if (strlen(full_name) > 0) {
                    strcat(full_name, " ");
                }
                strcat(full_name, first_name->family[i]);
            }
        }
    }
    
    return full_name;
}

bool fhir_patient_is_active(const FHIRPatient* patient) {
    if (!patient || !patient->active) {
        return true; // Default to active if not specified
    }
    return patient->active->value;
}

bool fhir_validate_patient(const FHIRPatient* patient) {
    if (!patient) return false;
    
    // Patient must have resourceType = "Patient"
    if (!patient->domain_resource.resource.resource_type || 
        strcmp(patient->domain_resource.resource.resource_type, "Patient") != 0) {
        return false;
    }
    
    // Validate gender if present
    if (patient->gender) {
        const char* valid_genders[] = {"male", "female", "other", "unknown"};
        bool valid_gender = false;
        for (int i = 0; i < 4; i++) {
            if (patient->gender && patient->gender->value && strcmp(patient->gender->value, valid_genders[i]) == 0) {
                valid_gender = true;
                break;
            }
        }
        if (!valid_gender) return false;
    }
    
    // Validate birthDate format if present
    if (patient->birth_date && patient->birth_date->value && !fhir_validate_date(patient->birth_date->value)) {
        return false;
    }
    
    return true;
}

const char* fhir_get_resource_type(const FHIRResource* resource) {
    return resource ? resource->resource_type : NULL;
}

bool fhir_is_foundation_resource(const char* resource_type) {
    if (!resource_type) return false;
    
    const char* foundation_types[] = {
        "Patient", "Practitioner", "PractitionerRole", "Organization", 
        "Location", "HealthcareService", "Endpoint", "RelatedPerson", 
        "Person", "Group"
    };
    
    for (int i = 0; i < 10; i++) {
        if (strcmp(resource_type, foundation_types[i]) == 0) {
            return true;
        }
    }
    
    return false;
}
// Additional Foundation Resource implementations

// CodeSystem Resource functions
FHIRCodeSystem* fhir_code_system_create(const char* id) {
    FHIRCodeSystem* code_system = calloc(1, sizeof(FHIRCodeSystem));
    if (code_system) {
        code_system->domain_resource.resource.resource_type = fhir_string_duplicate("CodeSystem");
        code_system->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return code_system;
}

void fhir_code_system_free(FHIRCodeSystem* code_system) {
    if (code_system) {
        fhir_domain_resource_free(&code_system->domain_resource);
        
        fhir_uri_free(code_system->url);
        fhir_string_free((char*)code_system->version);
        fhir_string_free((char*)code_system->name);
        fhir_string_free((char*)code_system->title);
        fhir_code_free(code_system->status);
        if (code_system->experimental) free(code_system->experimental);
        fhir_datetime_free(code_system->date);
        fhir_string_free((char*)code_system->publisher);
        fhir_markdown_free(code_system->description);
        fhir_markdown_free(code_system->purpose);
        fhir_markdown_free(code_system->copyright);
        if (code_system->case_sensitive) free(code_system->case_sensitive);
        fhir_canonical_free(code_system->value_set);
        fhir_code_free(code_system->hierarchy_meaning);
        if (code_system->compositional) free(code_system->compositional);
        if (code_system->version_needed) free(code_system->version_needed);
        fhir_code_free(code_system->content);
        fhir_canonical_free(code_system->supplements);
        if (code_system->count) free(code_system->count);
        
        // Free identifiers
        if (code_system->identifier) {
            for (size_t i = 0; i < code_system->identifier_count; i++) {
                free(code_system->identifier[i]);
            }
            free(code_system->identifier);
        }
        
        // Free contacts
        if (code_system->contact) {
            for (size_t i = 0; i < code_system->contact_count; i++) {
                free(code_system->contact[i]);
            }
            free(code_system->contact);
        }
        
        // Free concepts
        if (code_system->concept) {
            for (size_t i = 0; i < code_system->concept_count; i++) {
                free(code_system->concept[i]);
            }
            free(code_system->concept);
        }
        
        free(code_system);
    }
}

FHIRCodeSystem* fhir_parse_code_system(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) return NULL;
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || strcmp(resource_type->valuestring, "CodeSystem") != 0) {
        return NULL;
    }
    
    cJSON* id = cJSON_GetObjectItemCaseSensitive(json, "id");
    const char* id_str = cJSON_IsString(id) ? id->valuestring : NULL;
    
    FHIRCodeSystem* code_system = fhir_code_system_create(id_str);
    if (!code_system) return NULL;
    
    // Parse basic fields
    cJSON* url = cJSON_GetObjectItemCaseSensitive(json, "url");
    if (cJSON_IsString(url)) {
        code_system->url = (FHIRUri*)fhir_string_duplicate(url->valuestring);
    }
    
    cJSON* version = cJSON_GetObjectItemCaseSensitive(json, "version");
    if (cJSON_IsString(version)) {
        code_system->version = (FHIRString*)fhir_string_duplicate(version->valuestring);
    }
    
    cJSON* name = cJSON_GetObjectItemCaseSensitive(json, "name");
    if (cJSON_IsString(name)) {
        code_system->name = (FHIRString*)fhir_string_duplicate(name->valuestring);
    }
    
    cJSON* title = cJSON_GetObjectItemCaseSensitive(json, "title");
    if (cJSON_IsString(title)) {
        code_system->title = (FHIRString*)fhir_string_duplicate(title->valuestring);
    }
    
    cJSON* status = cJSON_GetObjectItemCaseSensitive(json, "status");
    if (cJSON_IsString(status)) {
        code_system->status = (FHIRCode*)fhir_string_duplicate(status->valuestring);
    }
    
    cJSON* content = cJSON_GetObjectItemCaseSensitive(json, "content");
    if (cJSON_IsString(content)) {
        code_system->content = (FHIRCode*)fhir_string_duplicate(content->valuestring);
    }
    
    return code_system;
}

cJSON* fhir_code_system_to_json(const FHIRCodeSystem* code_system) {
    if (!code_system) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    cJSON_AddStringToObject(json, "resourceType", "CodeSystem");
    
    if (code_system->domain_resource.resource.id) {
        cJSON_AddStringToObject(json, "id", code_system->domain_resource.resource.id);
    }
    
    if (code_system->url) {
        cJSON_AddStringToObject(json, "url", (const char*)code_system->url);
    }
    
    if (code_system->version) {
        cJSON_AddStringToObject(json, "version", (const char*)code_system->version);
    }
    
    if (code_system->name) {
        cJSON_AddStringToObject(json, "name", (const char*)code_system->name);
    }
    
    if (code_system->title) {
        cJSON_AddStringToObject(json, "title", (const char*)code_system->title);
    }
    
    if (code_system->status) {
        cJSON_AddStringToObject(json, "status", (const char*)code_system->status);
    }
    
    if (code_system->content) {
        cJSON_AddStringToObject(json, "content", (const char*)code_system->content);
    }
    
    return json;
}

// ValueSet Resource functions
FHIRValueSet* fhir_value_set_create(const char* id) {
    FHIRValueSet* value_set = calloc(1, sizeof(FHIRValueSet));
    if (value_set) {
        value_set->domain_resource.resource.resource_type = fhir_string_duplicate("ValueSet");
        value_set->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return value_set;
}

void fhir_value_set_free(FHIRValueSet* value_set) {
    if (value_set) {
        fhir_domain_resource_free(&value_set->domain_resource);
        
        fhir_string_free(value_set->url);
        fhir_string_free(value_set->version);
        fhir_string_free(value_set->name);
        fhir_string_free(value_set->title);
        fhir_string_free(value_set->status);
        if (value_set->experimental) free(value_set->experimental);
        fhir_string_free(value_set->date);
        fhir_string_free(value_set->publisher);
        fhir_string_free(value_set->description);
        if (value_set->immutable) free(value_set->immutable);
        fhir_string_free(value_set->purpose);
        fhir_string_free(value_set->copyright);
        
        // Free compose and expansion structures
        if (value_set->compose) free(value_set->compose);
        if (value_set->expansion) free(value_set->expansion);
        
        free(value_set);
    }
}

// ConceptMap Resource functions
FHIRConceptMap* fhir_concept_map_create(const char* id) {
    FHIRConceptMap* concept_map = calloc(1, sizeof(FHIRConceptMap));
    if (concept_map) {
        concept_map->domain_resource.resource.resource_type = fhir_string_duplicate("ConceptMap");
        concept_map->domain_resource.resource.id = fhir_string_duplicate(id);
    }
    return concept_map;
}

void fhir_concept_map_free(FHIRConceptMap* concept_map) {
    if (concept_map) {
        fhir_domain_resource_free(&concept_map->domain_resource);
        
        fhir_string_free(concept_map->url);
        fhir_string_free(concept_map->version);
        fhir_string_free(concept_map->name);
        fhir_string_free(concept_map->title);
        fhir_string_free(concept_map->status);
        if (concept_map->experimental) free(concept_map->experimental);
        fhir_string_free(concept_map->date);
        fhir_string_free(concept_map->publisher);
        fhir_string_free(concept_map->description);
        fhir_string_free(concept_map->purpose);
        fhir_string_free(concept_map->copyright);
        fhir_string_free(concept_map->source_uri);
        fhir_string_free(concept_map->source_canonical);
        fhir_string_free(concept_map->target_uri);
        fhir_string_free(concept_map->target_canonical);
        
        // Free groups
        if (concept_map->group) {
            for (size_t i = 0; i < concept_map->group_count; i++) {
                free(concept_map->group[i]);
            }
            free(concept_map->group);
        }
        
        free(concept_map);
    }
}

// Binary Resource functions
FHIRBinary* fhir_binary_create(const char* id) {
    FHIRBinary* binary = calloc(1, sizeof(FHIRBinary));
    if (binary) {
        binary->resource.resource_type = fhir_string_duplicate("Binary");
        binary->resource.id = fhir_string_duplicate(id);
    }
    return binary;
}

void fhir_binary_free(FHIRBinary* binary) {
    if (binary) {
        fhir_resource_free(&binary->resource);
        
        fhir_string_free(binary->content_type);
        if (binary->security_context) free(binary->security_context);
        fhir_string_free(binary->data);
        
        free(binary);
    }
}

FHIRBinary* fhir_parse_binary(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) return NULL;
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || strcmp(resource_type->valuestring, "Binary") != 0) {
        return NULL;
    }
    
    cJSON* id = cJSON_GetObjectItemCaseSensitive(json, "id");
    const char* id_str = cJSON_IsString(id) ? id->valuestring : NULL;
    
    FHIRBinary* binary = fhir_binary_create(id_str);
    if (!binary) return NULL;
    
    cJSON* content_type = cJSON_GetObjectItemCaseSensitive(json, "contentType");
    if (cJSON_IsString(content_type)) {
        binary->content_type = fhir_string_duplicate(content_type->valuestring);
    }
    
    cJSON* data = cJSON_GetObjectItemCaseSensitive(json, "data");
    if (cJSON_IsString(data)) {
        binary->data = fhir_string_duplicate(data->valuestring);
    }
    
    return binary;
}

cJSON* fhir_binary_to_json(const FHIRBinary* binary) {
    if (!binary) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    cJSON_AddStringToObject(json, "resourceType", "Binary");
    
    if (binary->resource.id) {
        cJSON_AddStringToObject(json, "id", binary->resource.id);
    }
    
    if (binary->content_type) {
        cJSON_AddStringToObject(json, "contentType", binary->content_type);
    }
    
    if (binary->data) {
        cJSON_AddStringToObject(json, "data", binary->data);
    }
    
    return json;
}

// Bundle Resource functions
FHIRBundle* fhir_bundle_create(const char* id) {
    FHIRBundle* bundle = calloc(1, sizeof(FHIRBundle));
    if (bundle) {
        bundle->resource.resource_type = fhir_string_duplicate("Bundle");
        bundle->resource.id = fhir_string_duplicate(id);
    }
    return bundle;
}

void fhir_bundle_free(FHIRBundle* bundle) {
    if (bundle) {
        fhir_resource_free(&bundle->resource);
        
        if (bundle->identifier) free(bundle->identifier);
        fhir_string_free(bundle->type);
        fhir_string_free(bundle->timestamp);
        if (bundle->total) free(bundle->total);
        
        // Free links
        if (bundle->link) {
            for (size_t i = 0; i < bundle->link_count; i++) {
                free(bundle->link[i]);
            }
            free(bundle->link);
        }
        
        // Free entries
        if (bundle->entry) {
            for (size_t i = 0; i < bundle->entry_count; i++) {
                if (bundle->entry[i]->resource) {
                    fhir_resource_free(bundle->entry[i]->resource);
                }
                free(bundle->entry[i]);
            }
            free(bundle->entry);
        }
        
        if (bundle->signature) free(bundle->signature);
        
        free(bundle);
    }
}

FHIRBundle* fhir_parse_bundle(cJSON* json) {
    if (!json || !cJSON_IsObject(json)) return NULL;
    
    cJSON* resource_type = cJSON_GetObjectItemCaseSensitive(json, "resourceType");
    if (!cJSON_IsString(resource_type) || strcmp(resource_type->valuestring, "Bundle") != 0) {
        return NULL;
    }
    
    cJSON* id = cJSON_GetObjectItemCaseSensitive(json, "id");
    const char* id_str = cJSON_IsString(id) ? id->valuestring : NULL;
    
    FHIRBundle* bundle = fhir_bundle_create(id_str);
    if (!bundle) return NULL;
    
    cJSON* type = cJSON_GetObjectItemCaseSensitive(json, "type");
    if (cJSON_IsString(type)) {
        bundle->type = fhir_string_duplicate(type->valuestring);
    }
    
    cJSON* timestamp = cJSON_GetObjectItemCaseSensitive(json, "timestamp");
    if (cJSON_IsString(timestamp)) {
        bundle->timestamp = fhir_string_duplicate(timestamp->valuestring);
    }
    
    cJSON* total = cJSON_GetObjectItemCaseSensitive(json, "total");
    if (cJSON_IsNumber(total)) {
        bundle->total = fhir_integer_create((int)total->valuedouble);
    }
    
    // Parse entries
    cJSON* entry_array = cJSON_GetObjectItemCaseSensitive(json, "entry");
    if (cJSON_IsArray(entry_array)) {
        int array_size = cJSON_GetArraySize(entry_array);
        if (array_size > 0) {
            bundle->entry = calloc(array_size, sizeof(BundleEntry*));
            bundle->entry_count = 0;
            
            cJSON* entry_item = NULL;
            cJSON_ArrayForEach(entry_item, entry_array) {
                BundleEntry* entry = calloc(1, sizeof(BundleEntry));
                if (entry) {
                    cJSON* full_url = cJSON_GetObjectItemCaseSensitive(entry_item, "fullUrl");
                    if (cJSON_IsString(full_url)) {
                        entry->full_url = fhir_string_duplicate(full_url->valuestring);
                    }
                    
                    cJSON* resource = cJSON_GetObjectItemCaseSensitive(entry_item, "resource");
                    if (resource) {
                        entry->resource = fhir_parse_resource(resource);
                    }
                    
                    bundle->entry[bundle->entry_count++] = entry;
                }
            }
        }
    }
    
    return bundle;
}

cJSON* fhir_bundle_to_json(const FHIRBundle* bundle) {
    if (!bundle) return NULL;
    
    cJSON* json = cJSON_CreateObject();
    if (!json) return NULL;
    
    cJSON_AddStringToObject(json, "resourceType", "Bundle");
    
    if (bundle->resource.id) {
        cJSON_AddStringToObject(json, "id", bundle->resource.id);
    }
    
    if (bundle->type) {
        cJSON_AddStringToObject(json, "type", bundle->type);
    }
    
    if (bundle->timestamp) {
        cJSON_AddStringToObject(json, "timestamp", bundle->timestamp);
    }
    
    if (bundle->total) {
        cJSON_AddNumberToObject(json, "total", bundle->total->value);
    }
    
    // Add entries
    if (bundle->entry && bundle->entry_count > 0) {
        cJSON* entry_array = cJSON_CreateArray();
        for (size_t i = 0; i < bundle->entry_count; i++) {
            cJSON* entry_json = cJSON_CreateObject();
            
            if (bundle->entry[i]->full_url) {
                cJSON_AddStringToObject(entry_json, "fullUrl", bundle->entry[i]->full_url);
            }
            
            if (bundle->entry[i]->resource) {
                cJSON* resource_json = fhir_resource_to_json(bundle->entry[i]->resource);
                if (resource_json) {
                    cJSON_AddItemToObject(entry_json, "resource", resource_json);
                }
            }
            
            cJSON_AddItemToArray(entry_array, entry_json);
        }
        cJSON_AddItemToObject(json, "entry", entry_array);
    }
    
    return json;
}

// Utility functions
size_t fhir_bundle_get_entry_count(const FHIRBundle* bundle) {
    return bundle ? bundle->entry_count : 0;
}

FHIRResource* fhir_bundle_get_entry_resource(const FHIRBundle* bundle, size_t index) {
    if (!bundle || index >= bundle->entry_count || !bundle->entry[index]) {
        return NULL;
    }
    return bundle->entry[index]->resource;
}

bool fhir_bundle_add_entry(FHIRBundle* bundle, FHIRResource* resource, const char* full_url) {
    if (!bundle || !resource) return false;
    
    // Reallocate entry array
    BundleEntry** new_entries = realloc(bundle->entry, (bundle->entry_count + 1) * sizeof(BundleEntry*));
    if (!new_entries) return false;
    
    bundle->entry = new_entries;
    
    // Create new entry
    BundleEntry* entry = calloc(1, sizeof(BundleEntry));
    if (!entry) return false;
    
    entry->resource = resource;
    if (full_url) {
        entry->full_url = fhir_string_duplicate(full_url);
    }
    
    bundle->entry[bundle->entry_count++] = entry;
    
    // Update total if present
    if (bundle->total) {
        bundle->total->value = bundle->entry_count;
    }
    
    return true;
}

bool fhir_validate_code_system(const FHIRCodeSystem* code_system) {
    if (!code_system) return false;
    
    // Must have resourceType = "CodeSystem"
    if (!code_system->domain_resource.resource.resource_type || 
        strcmp(code_system->domain_resource.resource.resource_type, "CodeSystem") != 0) {
        return false;
    }
    
    // Must have status
    if (!code_system->status) return false;
    
    // Must have content
    if (!code_system->content) return false;
    
    return true;
}

bool fhir_validate_value_set(const FHIRValueSet* value_set) {
    if (!value_set) return false;
    
    // Must have resourceType = "ValueSet"
    if (!value_set->domain_resource.resource.resource_type || 
        strcmp(value_set->domain_resource.resource.resource_type, "ValueSet") != 0) {
        return false;
    }
    
    // Must have status
    if (!value_set->status) return false;
    
    return true;
}

bool fhir_validate_bundle(const FHIRBundle* bundle) {
    if (!bundle) return false;
    
    // Must have resourceType = "Bundle"
    if (!bundle->resource.resource_type || 
        strcmp(bundle->resource.resource_type, "Bundle") != 0) {
        return false;
    }
    
    // Must have type
    if (!bundle->type) return false;
    
    return true;
}

bool fhir_is_terminology_resource(const char* resource_type) {
    if (!resource_type) return false;
    
    const char* terminology_types[] = {
        "CodeSystem", "ValueSet", "ConceptMap", "NamingSystem"
    };
    
    for (int i = 0; i < 4; i++) {
        if (strcmp(resource_type, terminology_types[i]) == 0) {
            return true;
        }
    }
    
    return false;
}

// Duplicate function removed